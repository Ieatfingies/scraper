import time
import requests

SUBREDDITS = ["slavelabour", "doneDirtCheap", "forhire"]
KEYWORDS = ["python", "script", "web", "html", "css", "js", "svelte", "bot", "scrape", "api", "bug", "fix", "data", "database"]
HEADERS = {"User-Agent": "desktop:gig-scraper:v1.0 (by /u/your_username)"}

SUPABASE_URL = "https://lyofifkmhhlatybkqydl.supabase.co/rest/v1/gigs"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx5b2ZpZmttaGhsYXR5YmtxeWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTMzNjY0ODksImV4cCI6MjEwODk0MjQ4OX0.Va99aGzwS-tyUHyD61iMED2FZfv0FRcm5SPUQlsGZ3c"

DB_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

seen_ids = set()

def fetch_tasks():
    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=15"
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                continue
            
            data = res.json()
            posts = data.get("data", {}).get("children", [])
            
            for p in posts:
                item = p.get("data", {})
                post_id = item.get("id")
                title = item.get("title", "")
                link = f"https://reddit.com{item.get('permalink')}"
                created = item.get("created_utc")

                if post_id in seen_ids:
                    continue
                seen_ids.add(post_id)

                title_lower = title.lower()
                if "task" in title_lower or sub == "doneDirtCheap":
                    if any(kw in title_lower for kw in KEYWORDS):
                        print(f"[MATCH FOUND] {title}")

                        payload = {
                            "id": post_id,
                            "title": title,
                            "link": link,
                            "subreddit": sub,
                            "created": created
                        }
                        try:
                            requests.post(SUPABASE_URL, json=payload, headers=DB_HEADERS)
                        except Exception as e:
                            print(f"Supabase write failed: {e}")

        except Exception as e:
            print(f"Fetch error: {e}")

if __name__ == "__main__":
    while True:
        fetch_tasks()
        time.sleep(30)