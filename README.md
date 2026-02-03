# AI News Digest

A minimal static microsite that aggregates AI news summaries from public RSS feeds.

## Structure
```
ai-news-site/
├── content/articles/   # JSON files (one per article)
├── public/             # Generated static site
├── scripts/
│   ├── fetch_news.py   # Fetches news from RSS feeds
│   └── build.py        # Builds static HTML
├── templates/
│   └── index.html      # HTML template
└── requirements.txt
```

## Usage

```bash
pip install -r requirements.txt
python scripts/fetch_news.py   # Fetch new articles
python scripts/build.py        # Generate static site
```

## For Automated Agents

1. Run `python scripts/fetch_news.py`
2. Run `python scripts/build.py`
3. Commit and push changes

Content stored as JSON in `content/articles/`.
