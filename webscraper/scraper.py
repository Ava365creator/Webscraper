import json
import logging
from typing import List, Optional, Dict, Any

import requests
from bs4 import BeautifulSoup
from lxml import etree

log = logging.getLogger(__name__)


class ScraperError(Exception):
    pass


def fetch_url(url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> str:
    """Fetch a URL and return text content.

    Raises ScraperError on network problems or non-200 responses.
    """
    headers = headers or {"User-Agent": "webscraper/0.1 (+https://github.com/)"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        log.debug("Request failed", exc_info=e)
        raise ScraperError(f"Network error when fetching {url}: {e}")

    if resp.status_code != 200:
        raise ScraperError(f"Bad response {resp.status_code} when fetching {url}")
    return resp.text


def parse_html(content: str) -> BeautifulSoup:
    """Return a BeautifulSoup object parsed with lxml parser."""
    return BeautifulSoup(content, "lxml")


def parse_xml(content: str) -> etree._Element:
    """Return an lxml Element for XML content."""
    try:
        return etree.fromstring(content.encode("utf-8"))
    except (etree.XMLSyntaxError, ValueError) as e:
        raise ScraperError(f"Failed to parse XML: {e}")


def extract_by_css(html_content: str, selector: str, attribute: Optional[str] = None) -> List[str]:
    """Extract text or attribute values for elements matching a CSS selector.

    If attribute is None, returns element.text stripped. Otherwise returns element.get(attribute).
    """
    soup = parse_html(html_content)
    results: List[str] = []
    for el in soup.select(selector):
        if attribute:
            val = el.get(attribute)
            if val is not None:
                results.append(val)
        else:
            text = el.get_text(separator=" ")
            if text is not None:
                text = " ".join(part.strip() for part in text.split())
                if text:
                    results.append(text)
    return results


def extract_links(html_content: str) -> List[Dict[str, Any]]:
    """Return list of {href, text} for anchor tags found in HTML."""
    soup = parse_html(html_content)
    out: List[Dict[str, Any]] = []
    for a in soup.find_all("a"):
        href = a.get("href")
        text = " ".join(part.strip() for part in a.get_text(separator=" ").split())
        out.append({"href": href, "text": text})
    return out


def extract_by_xpath(xml_content: str, xpath: str) -> List[str]:
    """Evaluate an XPath expression against XML content and return string results."""
    root = parse_xml(xml_content)
    results: List[str] = []
    matches = root.xpath(xpath)
    for m in matches:
        if isinstance(m, etree._Element):
            text = ''.join(m.itertext()).strip()
            if text:
                results.append(text)
        else:
            # could be attribute or text value
            results.append(str(m))
    return results


def parse_html_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_xml_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def to_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
