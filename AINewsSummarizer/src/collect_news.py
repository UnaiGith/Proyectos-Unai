import requests
import pandas as pd
from datetime import date
import time

API_KEY = "929d5e92d35a45cbbf60ee79ab6afe94"  # replace with your actual key
BASE_URL = "https://newsapi.org/v2/everything"
PAGE_SIZE = 100
MAX_PAGES = 2   # per topic (2 x 100 = 200 per topic)
TOPICS = ["technology", "artificial intelligence", "finance", "politics", "science", "sports"]

def fetch_topic(topic):
    """Fetch multiple pages of news for a given topic."""
    all_articles = []
    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": topic,
            "language": "en",
            "pageSize": PAGE_SIZE,
            "page": page,
            "sortBy": "publishedAt",
            "apiKey": API_KEY
        }
        print(f"🔹 Fetching '{topic}' page {page}...")
        resp = requests.get(BASE_URL, params=params)
        data = resp.json()

        if data.get("status") != "ok" or not data.get("articles"):
            print(f"⚠️ No more results for '{topic}' (page {page}).")
            break

        all_articles.extend(data["articles"])
        time.sleep(1)  # small delay to avoid hitting rate limit

    return pd.DataFrame([
        {
            "topic": topic,
            "title": a.get("title"),
            "description": a.get("description"),
            "content": a.get("content"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
            "source": a.get("source", {}).get("name")
        }
        for a in all_articles
    ])

def collect_news():
    """Fetch news for multiple topics and merge into a single dataset."""
    all_dfs = []
    for topic in TOPICS:
        df_topic = fetch_topic(topic)
        if not df_topic.empty:
            all_dfs.append(df_topic)
        time.sleep(2)  # longer pause between topics (respect rate limit)

    if not all_dfs:
        print("⚠️ No articles retrieved at all.")
        return

    df = pd.concat(all_dfs, ignore_index=True).drop_duplicates(subset=["title", "url"])
    file_path = f"data/raw/news_{date.today()}.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Saved {len(df)} merged articles to {file_path}")

if __name__ == "__main__":
    collect_news()
