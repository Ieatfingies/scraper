import os
import time
import requests
import feedparser

SUBREDDITS = ["slavelabour", "doneDirtCheap", "forhire"]
KEYWORDS = [
    "python", "script", "web", "html", "css", "js", "svelte", "bot", 
    "scrape", "api", "bug", "fix", "data", "database", "developer", 
    "code", "coding", "automation", "backend", "frontend", "fullstack"
]

BUYING_TAGS = ["[task]", "[hiring]", "hiring", "task", "buying", "[buying]", "need"]

# Extra terms to exclude workers seeking jobs
SELLER_EXCLUSIONS = [
    "[offer]", "[for hire]", "for hire", "willing to take", 
    "need to earn", "looking for work", "available for"
]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
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

    for sub in SUBREDDITS:
        rss_url = f"https://www.reddit.com/r/{sub}/new.rss?limit=25"
        try:
            res = requests.get(rss_url, headers=HEADERS, timeout=10)
            
            # Backoff 10s if rate limited
            if res.status_code == 429:
                print(f"[RATE LIMITED] r/{sub} returned 429. Backing off 10s...")
                time.sleep(10)
                res = requests.get(rss_url, headers=HEADERS, timeout=10)

            if res.status_code != 200:
                print(f"[REDDIT ERROR] r/{sub} returned status code {res.status_code}")
                time.sleep(5)
                continue

            feed = feedparser.parse(res.text)
            entries = feed.entries
            print(f"Scanned {len(entries)} RSS posts from r/{sub}")

            for entry in entries:
                post_id = entry.get("id", "").split("/")[-1] or entry.get("link", "").split("/")[-2]
                title = entry.get("title", "")
                link = entry.get("link", "")

                if not post_id or post_id in seen_ids:
                    continue

                title_lower = title.lower()
                is_hiring_post = sub == "doneDirtCheap" or any(tag in title_lower for tag in BUYING_TAGS)
                is_offer_post = any(ex in title_lower for ex in SELLER_EXCLUSIONS)

                if is_hiring_post and not is_offer_post:
                    if any(kw in title_lower for kw in KEYWORDS):
                        seen_ids.add(post_id)
                        print(f"[MATCH FOUND] {title}")

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
            print(f"Fetch error for r/{sub}: {e}")

        # 5-second delay between subreddits to satisfy Reddit rate limits
        time.sleep(5)

if __name__ == "__main__":
    fetch_tasks()