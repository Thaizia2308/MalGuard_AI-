# data/fetch_real_data.py
import os
import requests
import pandas as pd

def fetch_openphish():
    """Fetch malicious URLs from OpenPhish (public feed)."""
    url = "https://openphish.com/feed.txt"
    r = requests.get(url, timeout=15)
    if r.status_code == 200:
        urls = [u.strip() for u in r.text.splitlines() if u.strip()]
        return urls
    return []

def fetch_safe_urls():
    """Generate safe URLs (common trusted domains)."""
    safe_sites = [
        "https://www.google.com", "https://www.microsoft.com",
        "https://www.github.com", "https://www.wikipedia.org",
        "https://www.reddit.com", "https://www.apple.com",
        "https://www.stackoverflow.com", "https://www.amazon.in",
        "https://www.tesla.com", "https://www.linkedin.com"
    ]
    return safe_sites

def build_dataset():
    malicious = fetch_openphish()
    safe = fetch_safe_urls()

    data = pd.DataFrame({
        "url": malicious + safe,
        "label": [1]*len(malicious) + [0]*len(safe)
    })

    # Ensure 'data' folder exists
    os.makedirs(os.path.join(os.path.dirname(__file__)), exist_ok=True)

    csv_path = os.path.join(os.path.dirname(__file__), "real_urls.csv")
    data.to_csv(csv_path, index=False)
    print(f"✅ Real dataset saved: {len(data)} URLs (Malicious={len(malicious)}, Safe={len(safe)})")
    return csv_path

if __name__ == "__main__":
    build_dataset()
