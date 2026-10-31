import os
import time
import requests
import feedparser

COMBINED_FEED_URL = "https://www.reddit.com/r/slavelabour+doneDirtCheap+forhire/new.rss?limit=50"

KEYWORDS = [
    "python", "script", "web", "html", "css", "js", "javascript", "typescript",
    "svelte", "react", "bot", "scrape", "scraper", "api", "bug", "fix", "data", 
    "database", "developer", "code", "coding", "automation", "backend", 
    "frontend", "fullstack", "excel", "sheets", "app", "site", "website", "program"
]

BUYING_TAGS = ["[task]", "[hiring]", "hiring", "task", "buying", "[buying]", "need"]

SELLER_EXCLUSIONS = [
    "[offer]", "[for hire]", "for hire", "willing to take", 
    "need to earn", "looking for work", "available for"
]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Unique User-Agent with timestamp to prevent Reddit edge caching
HEADERS = {
    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 GigScraperBot/{int(time.time())}"
}

DB_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

seen_ids = set()

def fetch_tasks():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] SUPABASE_URL or SUPABASE_KEY missing")
        return

    try:
        res = requests.get(COMBINED_FEED_URL, headers=HEADERS, timeout=15)
        
        if res.status_code == 429:
            print("[RATE LIMITED] Backing off 5s for single retry...")
            time.sleep(5)
            res = requests.get(COMBINED_FEED_URL, headers=HEADERS, timeout=15)

        if res.status_code != 200:
            print(f"[REDDIT ERROR] Feed returned status code {res.status_code}")
            return

        feed = feedparser.parse(res.text)
        entries = feed.entries
        print(f"Scanned {len(entries)} combined RSS posts")

        for entry in entries:
            link = entry.get("link", "")
            post_id = entry.get("id", "").split("/")[-1] or (link.split("/")[-2] if len(link.split("/")) > 2 else "")
            title = entry.get("title", "")

            # Extract exact subreddit from post link (e.g. /r/slavelabour/...)
            sub = "slavelabour"
            if "/r/" in link:
                sub = link.split("/r/")[1].split("/")[0]

            if not post_id or post_id in seen_ids:
                continue

            title_lower = title.lower()
            is_hiring_post = sub.lower() == "donedirtcheap" or any(tag in title_lower for tag in BUYING_TAGS)
            is_offer_post = any(ex in title_lower for ex in SELLER_EXCLUSIONS)

            if is_hiring_post and not is_offer_post:
                if any(kw in title_lower for kw in KEYWORDS):
                    seen_ids.add(post_id)
                    print(f"[MATCH FOUND] [{sub}] {title}")

                    payload = {
                        "id": post_id,
                        "title": title,
                        "link": link,
                        "subreddit": sub
                    }

                    db_res = requests.post(SUPABASE_URL, json=payload, headers=DB_HEADERS, timeout=10)
                    if db_res.status_code not in (200, 201):
                        print(f"[SUPABASE WRITE FAILED] Status {db_res.status_code}: {db_res.text}")
                    else:
                        print(f"[SUPABASE SUCCESS] Saved gig {post_id}")

    except Exception as e:
        print(f"Fetch error: {e}")

if __name__ == "__main__":
    fetch_tasks()