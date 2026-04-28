#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

README_PATH = Path("README.md")
START_MARKER = "<!-- DAILY-QUOTE-START -->"
END_MARKER = "<!-- DAILY-QUOTE-END -->"

API_BASE = "https://api.quotable.io"

# 你可以把这里改成更偏“哲学 / 物理”的关键词
SEARCH_TERMS = [
    "physics",
    "philosophy",
    "causality",
    "truth",
    "reason",
    "knowledge",
]


def fetch_json(url: str) -> dict | list:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (GitHub Actions daily quote updater)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = resp.read().decode("utf-8")
    return json.loads(payload)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def pick_quote() -> tuple[str, str, str]:
    # 先按主题搜索
    for term in SEARCH_TERMS:
        url = f"{API_BASE}/search/quotes?query={urllib.parse.quote(term)}&limit=20"
        try:
            data = fetch_json(url)
        except Exception:
            continue

        if isinstance(data, dict):
            results = data.get("results") or []
            if results:
                item = random.choice(results)
                content = item.get("content")
                author = item.get("author")
                if content and author:
                    return normalize_text(content), normalize_text(author), term

    # 再随机兜底
    try:
        data = fetch_json(f"{API_BASE}/quotes/random")
    except Exception:
        return (
            "The important thing is not to stop questioning.",
            "Albert Einstein",
            "local-fallback",
        )

    if isinstance(data, list):
        item = data[0]
    elif isinstance(data, dict):
        item = data
    else:
        raise ValueError("Unexpected response format from quote API.")

    content = item.get("content") or item.get("quote") or ""
    author = item.get("author") or item.get("a") or "Unknown"
    if not content:
        raise ValueError("Quote content missing from API response.")

    return normalize_text(content), normalize_text(author), "random"


def build_block(quote: str, author: str, source: str) -> str:
    return (
        f"{START_MARKER}\n"
        f"> **“{quote}”**\n"
        f"> — {author}\n"
        f"> _source: {source}_\n"
        f"{END_MARKER}"
    )


def main() -> int:
    if not README_PATH.exists():
        print("README.md not found.", file=sys.stderr)
        return 1

    content = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )

    if not pattern.search(content):
        print(
            f"Could not find {START_MARKER} ... {END_MARKER} block in README.md",
            file=sys.stderr,
        )
        return 1

    quote, author, source = pick_quote()
    new_block = build_block(quote, author, source)
    new_content = pattern.sub(new_block, content, count=1)

    if new_content != content:
        README_PATH.write_text(new_content, encoding="utf-8")
        print("README.md updated.")
    else:
        print("No changes needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())