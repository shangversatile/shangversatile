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

# Primary source: better filtering by authors/tags
QUOTABLE_BASE = "https://api.quotable.io"

# Backup sources
ZENQUOTES_RANDOM = "https://zenquotes.io/api/random"
FAVQS_QOTD = "https://favqs.com/api/qotd"

# Prefer authors related to physics, philosophy, mathematics, psychology, and literature.
# Not every API contains every author, so this is used as a preferred filter, not a guarantee.
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

# Tags supported by Quotable vary, so keep them broad and robust.
PREFERRED_TAGS = [
    "wisdom",
    "science",
    "famous-quotes",
    "knowledge",
    "philosophy",
    "literature",
]

MAX_QUOTE_LENGTH = 180

LOCAL_FALLBACK = (
    "The important thing is not to stop questioning.",
    "Albert Einstein",
    "local-fallback",
)


def fetch_json(url: str, retries: int = 2, timeout: int = 20) -> Any:
    """
    Fetch JSON with lightweight retry logic.
    This avoids failing immediately when an external quote API is temporarily unstable.
    """
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
                status = getattr(resp, "status", None)
                payload = resp.read().decode("utf-8")

            if status and status >= 400:
                raise RuntimeError(f"HTTP status {status}")

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

    # Avoid ZenQuotes occasional rate-limit / service messages.
    bad_phrases = [
        "too many requests",
        "zenquotes.io",
        "upgrade",
        "rate limit",
    ]

    lowered = quote.lower()
    return not any(bad in lowered for bad in bad_phrases)


def parse_quotable_item(item: dict[str, Any], source: str) -> tuple[str, str, str] | None:
    quote = item.get("content")
    author = item.get("author")

    if is_valid_quote(quote, author):
        return normalize_text(quote), normalize_text(author), source

    return None


def get_from_quotable_by_author() -> tuple[str, str, str] | None:
    """
    Try Quotable with preferred authors.
    This is the most targeted strategy for physics / philosophy / mathematics / literature.
    """
    authors = random.sample(PREFERRED_AUTHORS, k=min(6, len(PREFERRED_AUTHORS)))

    for author in authors:
        params = {
            "limit": "1",
            "maxLength": str(MAX_QUOTE_LENGTH),
            "author": author,
        }
        url = f"{QUOTABLE_BASE}/quotes/random?{urllib.parse.urlencode(params)}"

        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"[WARN] Quotable author source failed for {author}: {e}")
            continue

        if isinstance(data, list) and data:
            result = parse_quotable_item(data[0], f"quotable · author · {author}")
            if result:
                return result

        if isinstance(data, dict):
            result = parse_quotable_item(data, f"quotable · author · {author}")
            if result:
                return result

    return None


def get_from_quotable_by_tags() -> tuple[str, str, str] | None:
    """
    Try Quotable with broad tags.
    This is less precise than authors but still more relevant than fully random quotes.
    """
    random.shuffle(PREFERRED_TAGS)

    tag_query = "|".join(PREFERRED_TAGS[:4])
    params = {
        "limit": "5",
        "maxLength": str(MAX_QUOTE_LENGTH),
        "tags": tag_query,
    }
    url = f"{QUOTABLE_BASE}/quotes/random?{urllib.parse.urlencode(params)}"

    try:
        data = fetch_json(url)
    except Exception as e:
        print(f"[WARN] Quotable tag source failed: {e}")
        return None

    items: list[dict[str, Any]] = []

    if isinstance(data, list):
        items = [item for item in data if isinstance(item, dict)]
    elif isinstance(data, dict):
        items = [data]

    random.shuffle(items)

    for item in items:
        result = parse_quotable_item(item, f"quotable · tags · {tag_query}")
        if result:
            return result

    return None


def get_from_zenquotes() -> tuple[str, str, str] | None:
    """
    Backup API.
    ZenQuotes is less domain-specific but often useful as a stable secondary source.
    """
    try:
        data = fetch_json(ZENQUOTES_RANDOM)
    except Exception as e:
        print(f"[WARN] ZenQuotes failed: {e}")
        return None

    if isinstance(data, list) and data:
        item = data[0]
        if isinstance(item, dict):
            quote = item.get("q")
            author = item.get("a")

            if is_valid_quote(quote, author):
                return normalize_text(quote), normalize_text(author), "zenquotes"

    return None


def get_from_favqs_qotd() -> tuple[str, str, str] | None:
    """
    Final remote fallback.
    FavQs Quote of the Day does not require an API token.
    """
    try:
        data = fetch_json(FAVQS_QOTD)
    except Exception as e:
        print(f"[WARN] FavQs QOTD failed: {e}")
        return None

    if isinstance(data, dict):
        quote_obj = data.get("quote")

        if isinstance(quote_obj, dict):
            quote = quote_obj.get("body")
            author = quote_obj.get("author")

            if is_valid_quote(quote, author):
                return normalize_text(quote), normalize_text(author), "favqs · qotd"

    return None


def pick_quote() -> tuple[str, str, str]:
    """
    Multi-source strategy:
    1. Quotable by preferred authors
    2. Quotable by broad intellectual tags
    3. ZenQuotes random
    4. FavQs quote of the day
    5. Local hardcoded fallback
    """
    providers = [
        get_from_quotable_by_author,
        get_from_quotable_by_tags,
        get_from_zenquotes,
        get_from_favqs_qotd,
    ]

    for provider in providers:
        result = provider()
        if result:
            return result

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
