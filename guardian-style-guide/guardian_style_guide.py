#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "beautifulsoup4>=4.12.0",
#     "httpx>=0.27.0",
# ]
# ///
"""Download the Guardian and Observer style guide into Markdown batch files.

By default, fetches all letters in four alphabetical batches (a-f, g-l, m-r, s-z)
and writes them directly into the 'references/' directory.

Usage:
    uv run guardian_style_guide.py                     # Downloads all 4 batches to references/
    uv run guardian_style_guide.py --out full.md       # Downloads all letters into a single file
    uv run guardian_style_guide.py --letters z         # Downloads only letter z
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys
import time

from bs4 import BeautifulSoup, NavigableString, Tag
import httpx

PAGE_URL = "https://www.theguardian.com/guardian-style-guide-{letter}"
SERIES_URL = "https://www.theguardian.com/info/series/the-guardian-style-guide"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

DEFAULT_OUT_DIR = Path("references")
DEFAULT_BATCHES: list[tuple[str, str]] = [
    ("a-f", "abcdef"),
    ("g-l", "ghijkl"),
    ("m-r", "mnopqr"),
    ("s-z", "stuvwxyz"),
]


def el_to_md(el: Tag | NavigableString) -> str:
    """Convert an HTML tag or text node to clean Markdown."""
    if isinstance(el, NavigableString):
        text = str(el).replace("\xa0", " ")
        return re.sub(r"([\\`*_\[\]<>])", r"\\\1", text)

    if not isinstance(el, Tag):
        return ""

    if el.name in ("strong", "b"):
        inner = "".join(el_to_md(c) for c in el.children).strip()
        return f"**{inner}**" if inner else ""

    if el.name in ("em", "i"):
        inner = "".join(el_to_md(c) for c in el.children).strip()
        return f"*{inner}*" if inner else ""

    if el.name == "a":
        href = el.get("href", "")
        inner = "".join(el_to_md(c) for c in el.children).strip()
        if href and not href.startswith("#"):
            return f"[{inner}]({href})"
        return inner

    if el.name == "br":
        return "\n"

    if el.name in ("sub", "sup", "span"):
        return "".join(el_to_md(c) for c in el.children)

    return "".join(el_to_md(c) for c in el.children)


def format_p(p: Tag) -> list[str]:
    """Format a <p> element into one or more Markdown entries."""
    # Move any <br> accidentally nested inside <strong>/<em> out after the tag
    for br in p.find_all("br"):
        if br.parent.name in ("strong", "b", "em", "i"):
            br.parent.insert_after(br)

    md = el_to_md(p)
    md = re.sub(r"\*\*[ \t]*\*\*", " ", md)

    lines = [line.strip() for line in md.split("\n") if line.strip()]
    if not lines:
        return []

    # Group lines by bold headwords
    entries: list[list[str]] = []
    current: list[str] = [lines[0]]
    for line in lines[1:]:
        if line.startswith("**") and not line.startswith("** "):
            entries.append(current)
            current = [line]
        else:
            current.append(line)
    entries.append(current)

    result: list[str] = []
    for entry in entries:
        fixed_lines: list[str] = []
        for line in entry:
            if re.match(r"^(?:#{1,6}\s|[-+]\s|\d+[.)]\s|>)", line):
                line = "\\" + line
            fixed_lines.append(line)

        if len(fixed_lines) == 2 and fixed_lines[0].startswith("**"):
            result.append(f"{fixed_lines[0]} — {fixed_lines[1]}")
        else:
            result.append("\\\n".join(fixed_lines))

    return result


def parse_page(html: str) -> tuple[str, str]:
    """Extract (standfirst_quote, article_markdown) from a Guardian page."""
    soup = BeautifulSoup(html, "html.parser")

    # Extract opening standfirst quote if present
    standfirst = ""
    standfirst_el = soup.select_one('[data-gu-name="standfirst"]')
    if standfirst_el:
        quote = el_to_md(standfirst_el).strip()
        if quote:
            standfirst = "\n".join(f"> {line}" if line else ">" for line in quote.splitlines())

    # Extract article body
    body_el = soup.select_one(".article-body-commercial-selector")
    if not body_el:
        return standfirst, ""

    blocks: list[str] = []
    for p in body_el.find_all("p"):
        # Skip A-Z navigation bars (paragraphs with 15+ links to other guide letters)
        nav_links = p.find_all("a", href=re.compile(r"/guardian-(?:observer-)?style-guide-[a-z]"))
        if len(nav_links) >= 15:
            continue
        blocks.extend(format_p(p))

    return standfirst, "\n\n".join(blocks)


def fetch(url: str, *, attempts: int = 3, timeout: float = 30.0) -> str:
    """Download a webpage with retries."""
    for attempt in range(1, attempts + 1):
        try:
            resp = httpx.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=timeout,
                follow_redirects=True,
            )
            resp.raise_for_status()
            return resp.text
        except Exception as err:
            if attempt == attempts:
                raise RuntimeError(f"could not fetch {url}: {err}") from err
            time.sleep(2 ** (attempt - 1))

    raise RuntimeError(f"could not fetch {url}")


def build_document(letters: str, delay: float) -> str:
    """Build a complete Markdown document for the specified letters."""
    letter_sections: list[tuple[str, str]] = []
    total = len(letters)

    for index, letter in enumerate(letters, start=1):
        url = PAGE_URL.format(letter=letter)
        print(f"[{index:2d}/{total}] {letter.upper()} {url}", file=sys.stderr)
        html = fetch(url)
        standfirst, body = parse_page(html)
        if not body:
            raise RuntimeError(f"no article body found for {url}")

        if standfirst:
            section = f"## {letter.upper()}\n\n{standfirst}\n\n{body}"
        else:
            section = f"## {letter.upper()}\n\n{body}"

        letter_sections.append((letter.upper(), section))
        if index < total:
            time.sleep(delay)

    contents = " · ".join(
        f"[{letter}](#{letter.lower()})" for letter, _ in letter_sections
    )
    today = dt.date.today().isoformat()

    header = (
        "# Guardian and Observer Style Guide\n\n"
        f"Source: <{SERIES_URL}>\n\n"
        f"Retrieved: {today}\n\n"
        "## Contents\n\n"
        f"{contents}"
    )
    return header + "\n\n" + "\n\n".join(section for _, section in letter_sections) + "\n"


def write_document(dest: Path, content: str) -> None:
    """Atomically write text content to a destination file."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    temporary = dest.with_name(dest.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(dest)
    print(f"wrote {dest} ({len(content):,} characters)", file=sys.stderr)


def selftest() -> None:
    """Run offline verification of the HTML-to-Markdown parser."""
    nav = " ".join(
        f'<a href="/guardian-style-guide-{letter}">{letter.upper()}</a>'
        for letter in "abcdefghijklmnopqrstuvwxyz"
    )
    page = f"""
    <div data-gu-name="standfirst"><p>‘Quote.’ <strong>Author</strong></p></div>
    <div class="article-body-commercial-selector">
      <p>{nav}</p>
      <p><strong>A*</strong><br/>(A-level and GCSE) not A-star</p>
      <p><strong>term</strong><br>first line<br>second line</p>
      <p><strong>note</strong><br><em>italic</em></p>
    </div>
    """
    standfirst, body = parse_page(page)

    assert "guardian-style-guide-a" not in body
    assert "**A\\*** — (A-level and GCSE) not A-star" in body
    assert "**term**\\\nfirst line\\\nsecond line" in body
    assert "**note** — *italic*" in body
    assert standfirst == "> ‘Quote.’ **Author**"
    print("selftest passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the Guardian and Observer style guide in alphabetical batches."
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="output directory for batch files (default: references)",
    )
    parser.add_argument(
        "-o", "--out",
        type=Path,
        default=None,
        help="output a single combined Markdown file instead of batches",
    )
    parser.add_argument(
        "--letters",
        default=None,
        help="specific letters to download (e.g. 'abcdef' or 'z')",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.4,
        help="seconds between requests (default: 0.4)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run the offline parser test and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.selftest:
        selftest()
        return 0

    delay = max(0.0, args.delay)

    # Single-file or custom letters mode
    if args.letters or args.out:
        letters_raw = args.letters or "abcdefghijklmnopqrstuvwxyz"
        letters = "".join(char for char in letters_raw.lower() if char.isalpha())
        if not letters:
            print("error: --letters contains no valid letters", file=sys.stderr)
            return 2

        out_file = args.out or (args.out_dir / f"guardian-style-guide-{letters}.md")
        try:
            document = build_document(letters, delay)
            write_document(out_file, document)
        except Exception as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        return 0

    # Default: download all 4 batches into out_dir (references/)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    total_batches = len(DEFAULT_BATCHES)

    for b_idx, (batch_name, letters) in enumerate(DEFAULT_BATCHES, start=1):
        print(f"\n=== Batch [{b_idx}/{total_batches}]: {batch_name.upper()} ({letters}) ===", file=sys.stderr)
        out_file = args.out_dir / f"guardian-style-guide-{batch_name}.md"
        try:
            document = build_document(letters, delay)
            write_document(out_file, document)
        except Exception as error:
            print(f"error building batch {batch_name}: {error}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
