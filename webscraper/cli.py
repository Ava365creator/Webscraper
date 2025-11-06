"""Simple CLI for the webscraper package."""
import argparse
import sys
import json
from typing import Optional

from . import scraper


def main(argv: Optional[list] = None) -> int:
    p = argparse.ArgumentParser(prog="webscraper", description="Simple web scraper CLI")
    sub = p.add_subparsers(dest="command")

    # common args
    def add_common(parser):
        parser.add_argument("--type", choices=["html", "xml"], default="html", help="Content type")
        parser.add_argument("--selector", help="CSS selector (for HTML) or XPath (for XML)")
        parser.add_argument("--attribute", help="Attribute to extract for HTML selectors (e.g., href)")
        parser.add_argument("--extract-links", action="store_true", help="Extract links (HTML only)")
        parser.add_argument("--output", "-o", help="Path to save output as JSON (if omitted, prints to stdout)")

    url_cmd = sub.add_parser("from-url", help="Fetch content from URL")
    url_cmd.add_argument("--url", required=True, help="URL to fetch")
    add_common(url_cmd)

    file_cmd = sub.add_parser("from-file", help="Load content from local file")
    file_cmd.add_argument("--path", required=True, help="Local file path")
    add_common(file_cmd)

    args = p.parse_args(argv)

    try:
        if args.command == "from-url":
            content = scraper.fetch_url(args.url)
        elif args.command == "from-file":
            with open(args.path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            p.print_help()
            return 2

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
                return 3
            out = scraper.extract_by_xpath(content, args.selector)

        # If the user supplied an output path, save to file; otherwise print JSON to stdout
        if getattr(args, "output", None):
            try:
                scraper.save_json_to_file(out, args.output)
                print(f"Saved output to {args.output}")
            except Exception as e:
                print(f"Failed to save output: {e}", file=sys.stderr)
                return 1
        else:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
