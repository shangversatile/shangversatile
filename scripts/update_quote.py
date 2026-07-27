#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import json
import os
import random
import re
import signal
import socket
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

README_PATH = Path("README.md")

START_MARKER = "<!-- DAILY-QUOTE-START -->"
END_MARKER = "<!-- DAILY-QUOTE-END -->"

WIKIQUOTE_API = "https://en.wikiquote.org/w/api.php"

MAX_TOTAL_SECONDS = int(os.getenv("QUOTE_MAX_TOTAL_SECONDS", "35"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("QUOTE_REQUEST_TIMEOUT_SECONDS", "6"))
MAX_PAGES_PER_RUN = int(os.getenv("QUOTE_MAX_PAGES_PER_RUN", "3"))

# 调试阶段建议 False：远程失败就让 workflow 失败，不要用 fallback 假装成功。
ALLOW_FALLBACK_UPDATE = os.getenv("QUOTE_ALLOW_FALLBACK_UPDATE", "false").lower() == "true"

START_TIME = time.monotonic()

AUTHOR_PAGES = [
    {"title": "Albert Einstein", "field": "physics / philosophy"},
    {"title": "Richard Feynman", "field": "physics"},
    {"title": "Isaac Newton", "field": "physics / mathematics"},
    {"title": "Galileo Galilei", "field": "physics / mathematics"},
    {"title": "Niels Bohr", "field": "physics"},
    {"title": "Bertrand Russell", "field": "philosophy / logic"},
    {"title": "Immanuel Kant", "field": "philosophy"},
    {"title": "David Hume", "field": "philosophy / causality"},
    {"title": "Aristotle", "field": "philosophy"},
    {"title": "Ludwig Wittgenstein", "field": "philosophy / language"},
    {"title": "William James", "field": "psychology / philosophy"},
    {"title": "Blaise Pascal", "field": "mathematics / philosophy"},
    {"title": "Henri Poincare", "field": "mathematics / philosophy"},
    {"title": "William Shakespeare", "field": "literature"},
]

MIN_QUOTE_LENGTH = 30
MAX_QUOTE_LENGTH = 220

BANNED_TERMS = [
    "nation",
    "country",
    "government",
    "president",
    "empire",
    "war",
    "army",
    "revolution",
    "patriot",
    "politics",
    "political",
    "democracy",
    "republic",
    "constitution",
    "tyrant",
    "slavery",
    "citizen",
    "statesman",
    "election",
]

PREFERRED_TERMS = [
    "nature",
    "science",
    "physics",
    "mathematics",
    "mathematical",
    "geometry",
    "truth",
    "reason",
    "knowledge",
    "mind",
    "thought",
    "consciousness",
    "experience",
    "causality",
    "cause",
    "logic",
    "language",
    "world",
    "universe",
    "beauty",
    "poetry",
    "literature",
    "philosophy",
    "wisdom",
    "imagination",
    "reality",
    "understanding",
    "question",
]

SAFE_FALLBACK_QUOTES = [
    {
        "quote": "Nature is written in mathematical language.",
        "author": "Galileo Galilei",
        "field": "physics / mathematics",
        "source": "fallback · physics / mathematics",
    },
    {
        "quote": "The important thing is not to stop questioning.",
        "author": "Albert Einstein",
        "field": "physics / philosophy",
        "source": "fallback · physics / philosophy",
    },
    {
        "quote": "All men by nature desire to know.",
        "author": "Aristotle",
        "field": "philosophy",
        "source": "fallback · philosophy",
    },
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}", flush=True)


def elapsed_seconds() -> float:
    return time.monotonic() - START_TIME


def remaining_seconds() -> float:
    return MAX_TOTAL_SECONDS - elapsed_seconds()


def ensure_time_left(stage: str) -> None:
    if remaining_seconds() <= 0:
        raise TimeoutError(f"Global quote updater deadline exceeded during: {stage}")


def alarm_handler(signum: int, frame: object) -> None:
    raise TimeoutError("Hard process timeout reached.")


if hasattr(signal, "SIGALRM"):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(MAX_TOTAL_SECONDS + 5)

socket.setdefaulttimeout(REQUEST_TIMEOUT_SECONDS)


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_word(text: str, term: str) -> bool:
    return re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE) is not None


def fetch_json(url: str) -> Any:
    ensure_time_left("fetch_json:start")

    left = remaining_seconds()
    if left < 1.0:
        raise TimeoutError("Not enough time left for another HTTP request.")

    timeout = max(1.0, min(float(REQUEST_TIMEOUT_SECONDS), left))

    log("DEBUG", f"Fetching URL with timeout={timeout:.1f}s: {url}")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (GitHub Actions Wikiquote quote updater)",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        # 防止异常大页面导致 read 卡太久。
        payload = resp.read(2_000_000).decode("utf-8", errors="replace")

    ensure_time_left("fetch_json:after_read")
    return json.loads(payload)


def strip_nested_templates(text: str) -> str:
    previous = None
    current = text

    while previous != current:
        previous = current
        current = re.sub(r"\{\{[^{}]*\}\}", "", current)

    return current


def clean_wikitext(raw: str) -> str:
    text = raw

    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^>/]*/>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.IGNORECASE | re.DOTALL)

    text = strip_nested_templates(text)

    text = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)

    text = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", text)
    text = re.sub(r"\[https?://[^\]]+\]", "", text)

    text = re.sub(r"<[^>]+>", "", text)

    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"\[\d+\]", "", text)

    return normalize_text(text)


def fetch_wikiquote_wikitext(title: str) -> str:
    ensure_time_left(f"fetch_wikiquote_wikitext:{title}")

    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
        "redirects": "1",
    }

    url = f"{WIKIQUOTE_API}?{urllib.parse.urlencode(params)}"
    data = fetch_json(url)

    pages = data.get("query", {}).get("pages", [])

    if not isinstance(pages, list) or not pages:
        raise ValueError(f"No pages returned for title={title}")

    page = pages[0]

    if page.get("missing"):
        raise ValueError(f"Wikiquote page not found: {title}")

    revisions = page.get("revisions", [])

    if not revisions:
        raise ValueError(f"No revisions returned for title={title}")

    content = revisions[0].get("slots", {}).get("main", {}).get("content")

    if not content:
        raise ValueError(f"No wikitext content returned for title={title}")

    return str(content)


def extract_quote_candidates(wikitext: str) -> list[str]:
    ensure_time_left("extract_quote_candidates")

    candidates: list[str] = []

    for raw_line in wikitext.splitlines():
        line = raw_line.strip()

        if not line.startswith("*"):
            continue

        if line.startswith("**") or line.startswith("*:"):
            continue

        line = re.sub(r"^\*+\s*", "", line).strip()

        lowered = line.lower()

        if not line:
            continue

        if lowered.startswith(("see also", "external links", "references", "sourced", "unsourced")):
            continue

        if any(token in lowered for token in ["category:", "file:", "image:", "isbn", "http://", "https://"]):
            continue

        cleaned = clean_wikitext(line)

        if cleaned:
            candidates.append(cleaned)

    return candidates


def is_good_quote(quote: str) -> bool:
    q = normalize_text(quote)
    lowered = q.lower()

    if len(q) < MIN_QUOTE_LENGTH:
        return False

    if len(q) > MAX_QUOTE_LENGTH:
        return False

    bad_markup = ["{{", "}}", "[[", "]]", "<ref", "</ref>", "|"]
    if any(mark in q for mark in bad_markup):
        return False

    if q.count(";") >= 3 or q.count(":") >= 3:
        return False

    if any(contains_word(lowered, term) for term in BANNED_TERMS):
        return False

    if any(term in lowered for term in PREFERRED_TERMS):
        return True

    if 50 <= len(q) <= 160 and q.endswith((".", "!", "?")):
        return True

    return False


def pick_fallback_quote() -> dict[str, str]:
    today = dt.date.today().isoformat()
    rng = random.Random(today)
    return rng.choice(SAFE_FALLBACK_QUOTES)


def pick_quote_from_wikiquote() -> dict[str, str] | None:
    today = dt.date.today().isoformat()
    rng = random.Random(today)

    pages = AUTHOR_PAGES[:]
    rng.shuffle(pages)
    pages = pages[:MAX_PAGES_PER_RUN]

    log("INFO", f"Trying {len(pages)} Wikiquote pages. Global timeout={MAX_TOTAL_SECONDS}s.")

    for page in pages:
        ensure_time_left(f"page_loop:{page['title']}")

        title = page["title"]
        field = page["field"]

        log("INFO", f"Trying Wikiquote page: {title}")

        try:
            wikitext = fetch_wikiquote_wikitext(title)
            candidates = extract_quote_candidates(wikitext)
            good_quotes = [q for q in candidates if is_good_quote(q)]

            log(
                "INFO",
                f"{title}: {len(candidates)} candidates, {len(good_quotes)} passed filters.",
            )

            if not good_quotes:
                continue

            quote = rng.choice(good_quotes)

            return {
                "quote": quote,
                "author": title,
                "field": field,
                "source": "wikiquote",
            }

        except Exception as e:
            log("WARN", f"Failed on {title}: {type(e).__name__}: {e}")
            continue

    return None


def build_block(item: dict[str, str]) -> str:
    today = dt.date.today().isoformat()

    quote = item["quote"]
    author = item["author"]
    field = item["field"]
    source = item["source"]

    return (
        f"{START_MARKER}\n"
        f"> **“{quote}”**\n"
        f"> — {author}\n"
        f"> _field: {field} · source: {source}_\n"
        f"<!-- quote-updated: {today} -->\n"
        f"{END_MARKER}"
    )


def update_readme() -> bool:
    ensure_time_left("update_readme:start")

    if not README_PATH.exists():
        log("ERROR", "README.md not found.")
        return False

    content = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )

    if not pattern.search(content):
        log("ERROR", f"Could not find quote markers: {START_MARKER} ... {END_MARKER}")
        return False

    item = pick_quote_from_wikiquote()

    if item is None:
        if not ALLOW_FALLBACK_UPDATE:
            log(
                "ERROR",
                "No valid remote quote was found. README will not be updated with fallback.",
            )
            return False

        log("WARN", "No valid remote quote found. Using fallback because QUOTE_ALLOW_FALLBACK_UPDATE=true.")
        item = pick_fallback_quote()

    log(
        "INFO",
        f"Quote selected: {item['quote']} — {item['author']} "
        f"({item['field']} · {item['source']})",
    )

    new_block = build_block(item)
    new_content = pattern.sub(new_block, content, count=1)

    if new_content != content:
        README_PATH.write_text(new_content, encoding="utf-8")
        log("SUCCESS", "README.md updated.")
    else:
        log("INFO", "No changes needed.")

    return True


def main() -> int:
    try:
        ok = update_readme()
        return 0 if ok else 1
    except TimeoutError as e:
        log("ERROR", f"Timeout: {e}")
        return 124
    except Exception as e:
        log("ERROR", f"Unexpected failure: {type(e).__name__}: {e}")
        return 1
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
