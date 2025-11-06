# Webscraper

A small Python web scraping utility using requests, BeautifulSoup and lxml for HTML and XML extraction.

Features
- Fetch and parse HTML from a URL or local file
- Fetch and parse XML from a URL or local file
- CSS-selector based extraction, link extraction, and attribute extraction
- Small CLI to run scraping tasks and print JSON output

Requirements
- Python 3.8+
- See `requirements.txt`

Quick start (local)
1. Create a virtual environment and install dependencies:

```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run CLI on a URL:

```cmd
python -m webscraper.cli from-url --url "https://example.com" --selector "a" --attribute "href"
```

3. Run tests (requires pytest):

```cmd
pip install pytest
pytest -q
```

Push to your GitHub repo

To push this local project to your GitHub repo `https://github.com/Ava365creator/Webscraper.git`:

```cmd
cd "C:\Users\annem\OneDrive\Webscraper"
git init
git add .
git commit -m "Add webscraper project"
git remote add origin https://github.com/Ava365creator/Webscraper.git
git branch -M main
git push -u origin main
```

If the repo already exists and is empty, this will push the files. If credentials are needed, you'll be prompted.

Notes
- I did not push changes to GitHub automatically. If you want, I can run git commands locally — tell me and I'll proceed.
