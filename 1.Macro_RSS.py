import requests
import xml.etree.ElementTree as ET
import json
from urllib.parse import urlparse

# RSS feeds to combine
rss_feeds = {
    "Real World Assets": "https://www.google.co.uk/alerts/feeds/02987389766485843804/18248594531215203351",
    "RWA": "https://www.google.co.uk/alerts/feeds/02987389766485843804/9168224349089223068",
    "Tokenisation": "https://www.google.co.uk/alerts/feeds/02987389766485843804/10520499875665674304",
    "Tokenization": "https://www.google.co.uk/alerts/feeds/02987389766485843804/8484296043666868741",
    "Real-world assets": "https://www.google.co.uk/alerts/feeds/02987389766485843804/9196159844228789916",
    "Tokenized": "https://www.google.co.uk/alerts/feeds/02987389766485843804/3907847878136615686"
}


# Function to infer the source from the link
def infer_source(link):
    try:
        parsed_url = urlparse(link)
        domain_parts = parsed_url.netloc.split('.')
        if len(domain_parts) > 2:
            return domain_parts[-2].capitalize()  # Extract second-to-last part of the domain as source
        else:
            return domain_parts[0].capitalize()
    except Exception as e:
        print(f"Error inferring source: {e}")
        return "Unknown"


# Parse individual RSS feed
def parse_rss_feed(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        entries = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            google_link = entry.find("{http://www.w3.org/2005/Atom}link").attrib["href"]
            published = entry.find("{http://www.w3.org/2005/Atom}published").text if entry.find(
                "{http://www.w3.org/2005/Atom}published") is not None else "Unknown"
            content = entry.find("{http://www.w3.org/2005/Atom}content").text if entry.find(
                "{http://www.w3.org/2005/Atom}content") is not None else ""

            # Extract the cleaned link from Google redirect
            if "google.com/url" in google_link:
                parsed = urlparse(google_link)
                query_params = {kv.split('=')[0]: kv.split('=')[1] for kv in parsed.query.split('&') if '=' in kv}
                cleaned_link = query_params.get('url', google_link)
            else:
                cleaned_link = google_link

            # Infer the source
            source = infer_source(cleaned_link)

            entries.append({
                "title": title,
                "link": google_link,
                "cleaned_link": cleaned_link,
                "published": published,
                "content": content,
                "source": source
            })
        return entries
    except Exception as e:
        print(f"Error parsing feed {url}: {e}")
        return []


# Save the consolidated feed to JSON
def save_to_json(articles, output_file="9.G_Alerts_feed.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)
    print(f"Consolidated JSON feed saved to {output_file}")


# Main execution
if __name__ == "__main__":
    all_articles = []
    for topic, url in rss_feeds.items():
        print(f"Fetching feed for topic: {topic}")
        all_articles.extend(parse_rss_feed(url))

    print(f"Total articles consolidated: {len(all_articles)}")
    save_to_json(all_articles)
