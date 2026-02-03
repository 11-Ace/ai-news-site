# AI News Site - Agent Instructions

## Project Overview
A minimal static microsite that aggregates AI news summaries from RSS feeds.

## Update Workflow
To update the site with fresh content:
1. Run `python scripts/fetch_news.py` to fetch new articles
2. Run `python scripts/build.py` to regenerate HTML
3. Commit changes with message format: "Update AI news digest - [date]"
4. Push to origin

## Key Files
- `scripts/fetch_news.py` - Fetches news from RSS feeds, filters AI-related articles
- `scripts/build.py` - Generates static HTML from JSON content
- `content/articles/*.json` - Article data (auto-managed)
- `public/index.html` - Generated site output
- `templates/index.html` - HTML template

## Commands
- Update content: `python scripts/fetch_news.py && python scripts/build.py`
- Serve locally: `python -m http.server 8000 -d public`
- Commit: Include `Co-Authored-By: Warp <agent@warp.dev>` in commits
