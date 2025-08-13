# src/news_scraper.py
import os
import pandas as pd
import feedparser
from datetime import datetime, timezone

FEEDS = [
    # Reuters divisas (suele existir; si no, comenta esta)
    "https://feeds.reuters.com/reuters/forexNews",
    # DailyFX
    "https://www.dailyfx.com/feeds/all",
    # FXStreet (general)
    "https://www.fxstreet.com/rss",
    # Google News (consulta temática; ajusta palabras clave/idioma)
    "https://news.google.com/rss/search?q=forex+OR+FX+OR+currency+market+EUR+USD&hl=en&gl=US&ceid=US:en"
]

def collect_headlines(feeds=FEEDS):
    rows = []
    for url in feeds:
        feed = feedparser.parse(url)
        for e in feed.entries:
            rows.append({
                "source": feed.feed.get("title", ""),
                "title": e.get("title", "").strip(),
                "link": e.get("link", ""),
                "published": e.get("published", ""),
                "published_ts": e.get("published_parsed"),
            })
    df = pd.DataFrame(rows)
    if not df.empty:
        # Normaliza la fecha
        if "published_ts" in df.columns:
            df["published_utc"] = df["published_ts"].apply(
                lambda t: datetime(*t[:6], tzinfo=timezone.utc).isoformat() if t else None
            )
            df = df.drop(columns=["published_ts"])
        df = df.drop_duplicates(subset=["title"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = collect_headlines()
    out = "data/news_headlines.csv"
    df.to_csv(out, index=False)
    print(f"{len(df)} titulares guardados en: {out}")
