#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
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

# Primary + backup Quotable-compatible API bases.
# api.quotable.io may sometimes be unstable, so we keep a second Quotable deployment as backup.
QUOTABLE_BASES = [
    "https://api.quotable.io",
    "https://api.quotable.kurokeita.dev",
]

# Final remote fallback. Quote of the Day does not require an API token.
FAVQS_QOTD = "https://favqs.com/api/qotd"

# Broad intellectual tags. These are more reliable than very narrow tags.
PREFERRED_TAGS = [
    "science",
    "wisdom",
    "knowledge",
    "famous-quotes",
    "philosophy",
    "literature",
]

# Preferred authors related to physics, philosophy, mathematics, psychology, and literature.
# Not every API source contains all of them, so this is used as a preference, not a guarantee.
PREFERRED_AUTHORS = [
    "Albert Einstein",
    "Isaac Newton",
    "Galileo Galilei",
    "Richard Feynman",
    "Bertrand Russell",
    "Aristotle",
    "Plato",
    "Socrates",
    "Immanuel Kant",
    "David Hume",
    "Friedrich Nietzsche",
    "William James",
    "Carl Jung",
    "Blaise Pascal",
    "Henri Poincare",
    "William Shakespeare",
    "Fyodor Dostoevsky",
    "Virginia Woolf",
]

MAX_QUOTE_LENGTH = 180

LOCAL_FALLBACK = (
    "Nature is written in mathematical language.",
    "Galileo Galilei",
    "fallback · physics / mathematics",
)


def fetch_json(url: str, retries: int = 2, timeout: int = 20) -> Any:
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            print(f"[DEBUG] Fetching attempt {attempt}/{retries}: {url}")

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (GitHub Actions daily quote updater)",
                    "Accept": "application/json",
                },
            )

            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = resp.read().decode("utf-8")

            return json.loads(payload)

        except Exception as e:
            last_error = e
            print(f"[WARN] Fetch failed: {e}")
            time.sleep(1)

    raise RuntimeError(f"All fetch attempts failed. Last error: {last_error}")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def is_valid_quote(quote: str | None, author: str | None) -> bool:
    if not quote or not author:
        return False

    quote = normalize_text(quote)
    author = normalize_text(author)

    if len(quote) < 20:
        return False

    if len(quote) > MAX_QUOTE_LENGTH:
        return False

    bad_phrases = [
        "too many requests",
        "rate limit",
        "upgrade",
        "zenquotes",
        "zenquotes.io",
        "error",
        "not found",
    ]

    lowered = quote.lower()
    return not any(bad in lowered for bad in bad_phrases)


def parse_quotable_item(item: dict[str, Any], source: str) -> tuple[str, str, str] | None:
    quote = item.get("content")
    author = item.get("author")

    if is_valid_quote(quote, author):
        return normalize_text(str(quote)), normalize_text(str(author)), source

    return None


def parse_quotable_response(data: Any, source: str) -> tuple[str, str, str] | None:
    items: list[dict[str, Any]] = []

    if isinstance(data, list):
        items = [item for item in data if isinstance(item, dict)]
    elif isinstance(data, dict):
        # Some APIs return a single object, some return {"results": [...]}
        if isinstance(data.get("results"), list):
            items = [item for item in data["results"] if isinstance(item, dict)]
        else:
            items = [data]

    random.shuffle(items)

    for item in items:
        result = parse_quotable_item(item, source)
        if result:
            return result

    return None


def get_from_quotable_by_author() -> tuple[str, str, str] | None:
    authors = random.sample(PREFERRED_AUTHORS, k=min(6, len(PREFERRED_AUTHORS)))

    for base in QUOTABLE_BASES:
        for author in authors:
            params = {
                "limit": "3",
                "maxLength": str(MAX_QUOTE_LENGTH),
                "author": author,
            }

            # Quotable random endpoint.
            url = f"{base}/quotes/random?{urllib.parse.urlencode(params)}"

            try:
                data = fetch_json(url)
            except Exception as e:
                print(f"[WARN] Quotable author source failed: {base}, {author}: {e}")
                continue

            result = parse_quotable_response(data, f"quotable · author · {author}")
            if result:
                return result

    return None


def get_from_quotable_by_tags() -> tuple[str, str, str] | None:
    tags = PREFERRED_TAGS[:]
    random.shuffle(tags)

    # Use broad intellectual tags.
    selected_tags = tags[:4]
    tag_query = "|".join(selected_tags)

    for base in QUOTABLE_BASES:
        params = {
            "limit": "5",
            "maxLength": str(MAX_QUOTE_LENGTH),
            "tags": tag_query,
        }

        url = f"{base}/quotes/random?{urllib.parse.urlencode(params)}"

        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"[WARN] Quotable tag source failed: {base}: {e}")
            continue

        result = parse_quotable_response(data, f"quotable · tags · {tag_query}")
        if result:
            return result

    return None


def get_from_quotable_plain_random() -> tuple[str, str, str] | None:
    for base in QUOTABLE_BASES:
        params = {
            "maxLength": str(MAX_QUOTE_LENGTH),
        }

        # Try /random as another compatible pattern.
        url = f"{base}/random?{urllib.parse.urlencode(params)}"

        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"[WARN] Quotable plain random failed: {base}: {e}")
            continue

        result = parse_quotable_response(data, "quotable · random")
        if result:
            return result

    return None


def get_from_favqs_qotd() -> tuple[str, str, str] | None:
    try:
        data = fetch_json(FAVQS_QOTD)
    except Exception as e:
        print(f"[WARN] FavQs QOTD failed: {e}")
        return None

    if not isinstance(data, dict):
        return None

    quote_obj = data.get("quote")
    if not isinstance(quote_obj, dict):
        return None

    quote = quote_obj.get("body")
    author = quote_obj.get("author")

    if is_valid_quote(quote, author):
        return normalize_text(str(quote)), normalize_text(str(author)), "favqs · qotd"

    return None


def pick_quote() -> tuple[str, str, str]:
    providers = [
        get_from_quotable_by_author,
        get_from_quotable_by_tags,
        get_from_quotable_plain_random,
    ]

    for provider in providers:
        result = provider()
        if result:
            quote, author, source = result
            if is_topic_relevant(quote, author, source):
                return result
            print(f"[INFO] Rejected off-topic quote: {quote} — {author} ({source})")

    return LOCAL_FALLBACK


def build_block(quote: str, author: str, source: str) -> str:
    today = dt.date.today().isoformat()

    return (
        f"{START_MARKER}\n"
        f"> **“{quote}”**\n"
        f"> — {author}\n"
        f"> _source: {source}_\n"
        f"<!-- quote-updated: {today} -->\n"
        f"{END_MARKER}"
    )


def main() -> int:
    if not README_PATH.exists():
        print("[ERROR] README.md not found.", file=sys.stderr)
        return 1

    content = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )

    if not pattern.search(content):
        print(
            f"[ERROR] Could not find markers in README.md:\n"
            f"{START_MARKER} ... {END_MARKER}",
            file=sys.stderr,
        )
        return 1

    quote, author, source = pick_quote()
    print(f"[INFO] Quote selected: {quote} — {author} ({source})")

    new_block = build_block(quote, author, source)
    new_content = pattern.sub(new_block, content, count=1)

    if new_content != content:
        README_PATH.write_text(new_content, encoding="utf-8")
        print("[SUCCESS] README.md updated.")
    else:
        print("[INFO] No changes needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
