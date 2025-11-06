import sys
import pathlib

# Ensure the package directory is importable when tests are run from different CWDs
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from webscraper import scraper


SAMPLE_HTML = """<!doctype html>
<html>
  <head><title>Test page</title></head>
  <body>
    <h1>Heading</h1>
    <p class="intro">This is an intro.</p>
    <a href="/a">Link A</a>
    <a href="/b">Link B</a>
  </body>
</html>
"""


def test_extract_by_css_text():
    out = scraper.extract_by_css(SAMPLE_HTML, "p.intro")
    assert isinstance(out, list)
    assert out and "intro" in out[0]


def test_extract_by_css_attr():
    out = scraper.extract_by_css(SAMPLE_HTML, "a", attribute="href")
    assert out == ["/a", "/b"]


def test_extract_links():
    out = scraper.extract_links(SAMPLE_HTML)
    assert isinstance(out, list)
    assert any(item.get("href") == "/a" for item in out)
