import os
import time
import requests

SUBREDDITS = ["slavelabour", "doneDirtCheap", "forhire"]
KEYWORDS = [
    "python", "script", "web", "html", "css", "js", "svelte", "bot", 
    "scrape", "api", "bug", "fix", "data", "database", "developer", 
    "code", "coding", "automation", "backend", "frontend", "fullstack"
]

# Reddit intent tags
BUYING_TAGS = ["[task]", "[hiring]", "hiring", "task", "buying", "[buying]", "need"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 GigScraper/1.0"
}

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

DB_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

seen_ids = set()

def fetch_tasks():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] SUPABASE_URL or SUPABASE_KEY missing from environment variables!")
        return

    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=25"
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code != 200:
                print(f"[REDDIT ERROR] r/{sub} returned status code {res.status_code}")
                continue
            
            data = res.json()
            posts = data.get("data", {}).get("children", [])
            print(f"Scanned {len(posts)} posts from r/{sub}")
            
            for p in posts:
                item = p.get("data", {})
                post_id = item.get("id")
                title = item.get("title", "")
                link = f"https://reddit.com{item.get('permalink')}"
                created = item.get("created_utc")

                if not post_id or post_id in seen_ids:
                    continue

                title_lower = title.lower()

                # Check if post is a hiring/buying post
                is_hiring_post = sub == "doneDirtCheap" or any(tag in title_lower for tag in BUYING_TAGS)
                # Ignore selling/offer posts
                is_offer_post = "[offer]" in title_lower or "[for hire]" in title_lower or "for hire" in title_lower

                if is_hiring_post and not is_offer_post:
                    if any(kw in title_lower for kw in KEYWORDS):
                        seen_ids.add(post_id)
                        print(f"[MATCH FOUND] {title}")

                        payload = {
                            "id": post_id,
                            "title": title,
                            "link": link,
                            "subreddit": sub,
                            "created": created
                        }
                        
                        db_res = requests.post(SUPABASE_URL, json=payload, headers=DB_HEADERS, timeout=10)
                        if db_res.status_code not in (200, 201):
                            print(f"[SUPABASE WRITE FAILED] Status {db_res.status_code}: {db_res.text}")
                        else:
                            print(f"[SUPABASE SUCCESS] Saved gig {post_id}")

        except Exception as e:
            print(f"Fetch error for r/{sub}: {e}")

if __name__ == "__main__":
    fetch_tasks()