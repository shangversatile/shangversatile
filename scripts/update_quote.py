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

# ✅ 修复：API_BASE 只保留域名
API_BASE = "https://zenquotes.io/api/random"

SEARCH_TERMS = [
    "physics",
    "philosophy",
    "causality",
    "truth",
    "reason",
    "knowledge",
]


def fetch_json(url: str) -> dict | list:
    print(f"[DEBUG] Fetching: {url}")
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
    # ✅ 使用 ZenQuotes（更稳定）
    try:
        data = fetch_json("https://zenquotes.io/api/random")
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            content = item.get("q")
            author = item.get("a")
            if content and author:
                return normalize_text(content), normalize_text(author), "zenquotes"
    except Exception as e:
        print(f"[WARN] ZenQuotes failed: {e}")

    # ✅ fallback（保证有内容）
    return (
        "The important thing is not to stop questioning.",
        "Albert Einstein",
        "fallback",
    )

    # ✅ 2. 随机兜底（正确接口）
    try:
        data = fetch_json(f"{API_BASE}/random?tags=philosophy|science|famous-quotes")
        if isinstance(data, dict):
            content = data.get("content")
            author = data.get("author")
            if content and author:
                return normalize_text(content), normalize_text(author), "random"
    except Exception as e:
        print(f"[WARN] random API failed: {e}")

    # ✅ 3. 最终 fallback（保证一定有输出）
    return (
        "The important thing is not to stop questioning.",
        "Albert Einstein",
        "fallback",
    )


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
        print("[ERROR] README.md not found.", file=sys.stderr)
        return 1

    content = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.DOTALL,
    )

    if not pattern.search(content):
        print(
            f"[ERROR] Could not find markers in README.md:\n{START_MARKER} ... {END_MARKER}",
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
        print("[INFO] No changes needed (same quote).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
