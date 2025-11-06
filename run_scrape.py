"""Standalone runner script for the webscraper package.

Usage examples (Windows/cmd.exe):

python run_scrape.py --url "https://example.com" --type html --selector "a" --attribute href --output links.json
python run_scrape.py --path "webscraper\\tests\\test_sample.html" --type html --selector "p.intro"
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from webscraper import scraper


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Small runner script for webscraper package")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL to fetch")
    group.add_argument("--path", help="Local file path to read HTML/XML from")

    p.add_argument("--type", choices=["html", "xml"], default="html", help="Content type")
    p.add_argument("--selector", help="CSS selector (for HTML) or XPath (for XML)")
    p.add_argument("--attribute", help="Attribute to extract for HTML selectors (e.g., href)")
    p.add_argument("--extract-links", action="store_true", help="Extract links (HTML only)")
    p.add_argument("--output", "-o", help="Path to save output as JSON (if omitted, prints to stdout)")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.url:
            content = scraper.fetch_url(args.url)
        else:
            # read from local file
            with open(args.path, "r", encoding="utf-8") as f:
                content = f.read()

        # choose extraction mode
        if args.type == "html":
            if args.extract_links:
                out = scraper.extract_links(content)
            elif args.selector:
                out = scraper.extract_by_css(content, args.selector, attribute=args.attribute)
            else:
                # default: return page title
                soup = scraper.parse_html(content)
                title = soup.title.string if soup.title else None
                out = {"title": title}
        else:  # xml
            if not args.selector:
                print("XML mode requires --selector (an XPath).", file=sys.stderr)
                return 2
            out = scraper.extract_by_xpath(content, args.selector)

        # output
        if args.output:
            scraper.save_json_to_file(out, args.output)
            print(f"Saved output to {args.output}")
        else:
            import json

            print(json.dumps(out, ensure_ascii=False, indent=2))

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
