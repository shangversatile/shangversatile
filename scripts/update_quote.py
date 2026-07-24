#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import json
import random
import re
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

# 固定抓取这些页面，避免随机 API 把内容带偏。
# field 用于 README 里展示方向。
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
    {"title": "Plato", "field": "philosophy"},
    {"title": "Friedrich Nietzsche", "field": "philosophy"},
    {"title": "Ludwig Wittgenstein", "field": "philosophy / language"},
    {"title": "William James", "field": "psychology / philosophy"},
    {"title": "Carl Jung", "field": "psychology"},
    {"title": "Blaise Pascal", "field": "mathematics / philosophy"},
    {"title": "Henri Poincare", "field": "mathematics / philosophy"},
    {"title": "William Shakespeare", "field": "literature"},
    {"title": "Fyodor Dostoevsky", "field": "literature / psychology"},
    {"title": "Virginia Woolf", "field": "literature"},
]

MIN_QUOTE_LENGTH = 30
MAX_QUOTE_LENGTH = 220

# 这些词容易把主页气质带到政治、国家、战争、政论方向，先过滤掉。
BANNED_TERMS = [
    "nation",
    "country",
    "government",
    "president",
    "king",
    "queen",
    "empire",
    "war",
    "army",
    "revolution",
    "liberty",
    "freedom",
    "patriot",
    "politics",
    "political",
    "democracy",
    "republic",
    "constitution",
    "lawgiver",
    "tyrant",
    "slave",
    "slavery",
    "citizen",
    "state",
    "statesman",
    "tax",
    "election",
]

# 这些词更符合你的主页方向：物理、哲学、数学、认识论、心智、文学。
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

# 只有远程抓取全部失败时才会使用。
# 这不是主要来源，只是防止 workflow 空跑或写入坏内容。
SAFE_FALLBACK_QUOTES = [
    {
        "quote": "The important thing is not to stop questioning.",
        "author": "Albert Einstein",
        "field": "physics / philosophy",
        "source": "safe-fallback",
    },
    {
        "quote": "Sapere aude.",
        "author": "Immanuel Kant",
        "field": "philosophy",
        "source": "safe-fallback",
    },
    {
        "quote": "All men by nature desire to know.",
        "author": "Aristotle",
        "field": "philosophy",
        "source": "safe-fallback",
    },
]


def fetch_json(url: str, timeout: int = 8, retries: int = 1) -> Any:
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            print(f"[DEBUG] Fetching attempt {attempt}/{retries}: {url}")

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (GitHub Actions Wikiquote quote updater)",
                    "Accept": "application/json",
                },
            )

            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = resp.read().decode("utf-8", errors="replace")

            return json.loads(payload)

        except Exception as e:
            last_error = e
            print(f"[WARN] Fetch failed: {type(e).__name__}: {e}")
            time.sleep(0.5)

    raise RuntimeError(f"Fetch failed. Last error: {last_error}")


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_nested_templates(text: str) -> str:
    """
    Remove simple MediaWiki templates like {{...}}.
    This is not a full wikitext parser, but it is enough for README quote cleanup.
    """
    previous = None
    current = text

    while previous != current:
        previous = current
        current = re.sub(r"\{\{[^{}]*\}\}", "", current)

    return current


def clean_wikitext(raw: str) -> str:
    text = raw

    # Remove comments and references.
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^>/]*/>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.IGNORECASE | re.DOTALL)

    # Remove common templates.
    text = strip_nested_templates(text)

    # Convert wiki links:
    # [[Page|display]] -> display
    # [[Page]] -> Page
    text = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)

    # Remove external links:
    # [http://example.com label] -> label
    # [http://example.com] -> ""
    text = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", text)
    text = re.sub(r"\[https?://[^\]]+\]", "", text)

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", "", text)

    # Remove bold / italic wiki markup.
    text = text.replace("'''", "").replace("''", "")

    # Remove remaining citation markers.
    text = re.sub(r"\[\d+\]", "", text)

    # Clean repeated spaces.
    text = normalize_text(text)

    return text


def fetch_wikiquote_wikitext(title: str) -> str:
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

    revision = revisions[0]
    slots = revision.get("slots", {})
    main_slot = slots.get("main", {})

    content = main_slot.get("content")

    if not content:
        raise ValueError(f"No wikitext content returned for title={title}")

    return str(content)


def extract_quote_candidates(wikitext: str) -> list[str]:
    candidates: list[str] = []

    for raw_line in wikitext.splitlines():
        line = raw_line.strip()

        # Main Wikiquote quotes commonly begin with a single "*".
        # Skip sub-bullets "**", section metadata, and empty lines.
        if not line.startswith("*"):
            continue

        if line.startswith("**") or line.startswith("*:"):
            continue

        # Remove leading bullet markers.
        line = re.sub(r"^\*+\s*", "", line).strip()

        # Skip obvious metadata / file / category / section artifacts.
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

    # Avoid quotes with too much leftover markup.
    bad_markup = ["{{", "}}", "[[", "]]", "<ref", "</ref>", "|"]
    if any(mark in q for mark in bad_markup):
        return False

    # Avoid lists or sentence fragments.
    if q.count(";") >= 3:
        return False

    if q.count(":") >= 3:
        return False

    # Avoid political direction.
    if any(term in lowered for term in BANNED_TERMS):
        return False

    # Prefer theme relevance. But do not make it too strict for literature authors.
    if any(term in lowered for term in PREFERRED_TERMS):
        return True

    # Accept clean aphoristic quotes even if they do not contain preferred keywords.
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

    # 限制最多请求 6 个页面，防止 GitHub Actions 卡太久。
    pages = pages[:6]

    for page in pages:
        title = page["title"]
        field = page["field"]

        try:
            wikitext = fetch_wikiquote_wikitext(title)
        except Exception as e:
            print(f"[WARN] Failed to fetch Wikiquote page {title}: {type(e).__name__}: {e}")
            continue

        candidates = extract_quote_candidates(wikitext)
        good_quotes = [q for q in candidates if is_good_quote(q)]

        print(
            f"[INFO] {title}: {len(candidates)} candidates, "
            f"{len(good_quotes)} passed filters."
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
    if not README_PATH.exists():
        print("[ERROR] README.md not found.", file=sys.stderr)
        return False

    content = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )

    if not pattern.search(content):
        print(
            f"[ERROR] Could not find quote markers in README.md:\n"
            f"{START_MARKER} ... {END_MARKER}",
            file=sys.stderr,
        )
        return False

    item = pick_quote_from_wikiquote()

    if item is None:
        print("[WARN] All Wikiquote sources failed. Using safe fallback.")
        item = pick_fallback_quote()

    print(
        f"[INFO] Quote selected: {item['quote']} — {item['author']} "
        f"({item['field']} · {item['source']})"
    )

    new_block = build_block(item)
    new_content = pattern.sub(new_block, content, count=1)

    if new_content != content:
        README_PATH.write_text(new_content, encoding="utf-8")
        print("[SUCCESS] README.md updated.")
    else:
        print("[INFO] No changes needed.")

    return True


def main() -> int:
    return 0 if update_readme() else 1


if __name__ == "__main__":
    raise SystemExit(main())
