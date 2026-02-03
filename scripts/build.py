#!/usr/bin/env python3
"""Builds the static site from content files."""

import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content" / "articles"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
PUBLIC_DIR = PROJECT_ROOT / "public"

def load_articles() -> list:
    articles = []
    for filepath in CONTENT_DIR.glob("*.json"):
        with open(filepath, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))
    articles.sort(key=lambda x: x.get('published', ''), reverse=True)
    return articles

def load_template(name: str) -> str:
    with open(TEMPLATE_DIR / name, 'r', encoding='utf-8') as f:
        return f.read()

def format_date(iso_date: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y")
    except:
        return iso_date[:10] if iso_date else "Unknown"

def generate_article_html(article: dict) -> str:
    return f'''<article class="article-card">
    <div class="article-meta">
        <span class="source">{article.get('source', 'Unknown')}</span>
        <span class="separator">•</span>
        <span class="date">{format_date(article.get('published', ''))}</span>
    </div>
    <h2><a href="{article.get('url', '#')}" target="_blank" rel="noopener">{article.get('title', 'Untitled')}</a></h2>
    <p class="summary">{article.get('summary', '')}</p>
</article>'''

def build_site():
    print("Building site...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    articles = load_articles()
    template = load_template("index.html")
    articles_html = "\n".join(generate_article_html(a) for a in articles)
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    html = template.replace("{{ARTICLES}}", articles_html)
    html = html.replace("{{LAST_UPDATED}}", now)
    html = html.replace("{{ARTICLE_COUNT}}", str(len(articles)))
    output_path = PUBLIC_DIR / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {output_path} with {len(articles)} articles")

if __name__ == "__main__":
    build_site()
