# generate_data.py

import csv
import random

safe_domains = [
    "google.com", "openai.com", "github.com",
    "wikipedia.org", "amazon.com"
]

mal_domains = [
    "free-money.com", "verify-login.info",
    "secure-paypal.xyz", "login-steal.ru"
]

# Safe URLs (label 0)
rows = [(f"https://{d}", 0) for d in safe_domains]

# Malicious URLs (label 1)
rows += [(f"http://{d}/login", 1) for d in mal_domains]

# Add some shortened and IP-based links (malicious)
rows += [(f"http://bit.ly/{random.randint(100, 999)}", 1) for _ in range(10)]
rows += [
    (f"http://{random.randint(1, 255)}."
     f"{random.randint(1, 255)}."
     f"{random.randint(1, 255)}."
     f"{random.randint(1, 255)}/", 1)
    for _ in range(5)
]

# Write to CSV
with open('sample_urls.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'label'])
    for url, label in rows:
        writer.writerow([url, label])

print('✅ Wrote sample_urls.csv successfully!')
