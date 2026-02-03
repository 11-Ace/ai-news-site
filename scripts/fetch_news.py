#!/usr/bin/env python3
"""
Fetches recent AI news from public RSS feeds and saves summaries as JSON.
"""

import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
import feedparser
from bs4 import BeautifulSoup

CONTENT_DIR = Path(__file__).parent.parent / "content" / "articles"
MAX_ARTICLES = 20

RSS_FEEDS = [
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "source": "TechCrunch"},
    {"url": "https://www.artificialintelligence-news.com/feed/", "source": "AI News"},
    {"url": "https://venturebeat.com/category/ai/feed/", "source": "VentureBeat"},
    {"url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "source": "Ars Technica"},
]

def clean_html(html_content: str) -> str:
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', text).strip()

def generate_summary(content: str, max_length: int = 200) -> str:
    content = clean_html(content)
    if len(content) <= max_length:
        return content
    truncated = content[:max_length]
    last_period = truncated.rfind('.')
    if last_period > max_length * 0.5:
        return truncated[:last_period + 1]
    return truncated.rsplit(' ', 1)[0] + "..."

def generate_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]

def fetch_feed(feed_config: dict) -> list:
    articles = []
    try:
        print(f"  Fetching {feed_config['source']}...")
        feed = feedparser.parse(feed_config["url"])
        for entry in feed.entries[:10]:
            content = ""
            if hasattr(entry, "content"):
                content = entry.content[0].value
            elif hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "description"):
                content = entry.description
            
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6]).isoformat()
            else:
                published = datetime.now().isoformat()
            
            articles.append({
                "id": generate_id(entry.link),
                "title": clean_html(entry.title),
                "url": entry.link,
                "source": feed_config["source"],
                "published": published,
                "summary": generate_summary(content),
                "fetched_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"  Error fetching {feed_config['source']}: {e}")
    return articles

def is_ai_related(article: dict) -> bool:
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'neural network',
                   'deep learning', 'chatgpt', 'gpt', 'llm', 'openai', 'anthropic',
                   'gemini', 'claude', 'robot', 'generative']
    text = (article['title'] + ' ' + article['summary']).lower()
    return any(keyword in text for keyword in ai_keywords)

def save_article(article: dict):
    filepath = CONTENT_DIR / f"{article['id']}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(article, f, indent=2, ensure_ascii=False)

def load_existing_ids() -> set:
    return {fp.stem for fp in CONTENT_DIR.glob("*.json")}

def cleanup_old_articles(keep_count: int = 50):
    articles = []
    for filepath in CONTENT_DIR.glob("*.json"):
        with open(filepath, 'r', encoding='utf-8') as f:
            articles.append((filepath, json.load(f).get('published', '')))
    articles.sort(key=lambda x: x[1], reverse=True)
    for filepath, _ in articles[keep_count:]:
        filepath.unlink()
        print(f"  Removed old: {filepath.name}")

def main():
    print("AI News Fetcher\n" + "=" * 40)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = load_existing_ids()
    all_articles = []
    
    print("\nFetching feeds...")
    for feed_config in RSS_FEEDS:
        all_articles.extend(fetch_feed(feed_config))
    
    print("\nProcessing articles...")
    new_count = 0
    for article in all_articles:
        if article['id'] not in existing_ids and is_ai_related(article):
            save_article(article)
            new_count += 1
            print(f"  + {article['title'][:60]}...")
    
    print(f"\nAdded {new_count} new articles")
    cleanup_old_articles(keep_count=MAX_ARTICLES)
    print("\nDone!")

if __name__ == "__main__":
    main()
