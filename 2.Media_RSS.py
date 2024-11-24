import requests
import feedparser
import json

# Disable SSL warnings (for disabling SSL verification)
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# RSS Feeds to consolidate
rss_feeds = {
    "CoinTelegraph": "https://cointelegraph.com/rss",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "BlockWorks": "https://blockworks.co/feed",
    "Decrypt": "https://decrypt.co/feed",
    "CryptoSlate": "https://cryptoslate.com/feed/",
    "BeInCrypto": "https://beincrypto.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/"
}


# Function to fetch feeds with SSL disabled
def fetch_feed(feed_url):
    try:
        response = requests.get(feed_url, verify=False, timeout=10)  # Disable SSL verification
        response.raise_for_status()
        return feedparser.parse(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed {feed_url}: {e}")
        return None


# Function to extract categories from <category> field
def extract_categories(entry):
    categories = []
    if "tags" in entry:  # Most feeds provide categories under the 'tags' key
        categories = [tag["term"] for tag in entry["tags"]]
    elif "category" in entry:  # Some feeds may have a direct 'category' field
        categories = [entry["category"]]
    return categories


# Function to fetch and normalize feeds
def fetch_and_normalize_feeds(feeds):
    articles = []
    for feed_name, feed_url in feeds.items():
        print(f"Fetching feed: {feed_name}")
        feed = fetch_feed(feed_url)
        if not feed or feed.bozo:
            print(f"Error parsing feed {feed_name}: {feed.bozo_exception if feed else 'Unknown error'}")
            continue

        for entry in feed.entries:
            categories = extract_categories(entry)
            articles.append({
                "source": feed_name,
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", "#"),
                "published": entry.get("published", "Unknown"),
                "summary": entry.get("summary", ""),
                "content": entry.get("content", [{"value": ""}])[0]["value"] if "content" in entry else "",
                "categories": categories
            })
    return articles


# Save all feeds to a consolidated JSON file
def save_to_json(data, filename="9. Media_consolidated_feeds.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Consolidated JSON saved to {filename}")


# Main execution
if __name__ == "__main__":
    print("Fetching and consolidating RSS feeds...")
    all_articles = fetch_and_normalize_feeds(rss_feeds)
    print(f"Fetched {len(all_articles)} articles.")

    save_to_json(all_articles)
