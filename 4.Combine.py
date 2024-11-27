import json
from datetime import datetime, timezone, timedelta
import re

# Input file paths
file1 = "9.G_Alerts_feed.json"  # Google Alerts
file2 = "9.Media_filtered_feeds.json"  # Media Feeds
company_list_file = "company_list.txt"  # List of company names

# Output file path
output_file = "9.Combined_Feeds.json"

# Keywords to check in the title
KEYWORDS = ["real world assets", "real-world assets", "RWA", "Tokenisation", "Tokenization", "Tokenized"]

# Trusted sources
TRUSTED_SOURCES = ["Cointelegraph", "Coindesk", "Blockworks", "TechCrunch", "Bybit", "Binance"]

# Load the company list from a .txt file
def load_company_list(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            companies = [line.strip().lower() for line in f if line.strip()]
        return companies
    except Exception as e:
        print(f"Error loading company list: {e}")
        return []

# Function to clean Google Alert links
def clean_google_link(google_link):
    try:
        match = re.search(r'url=(https?://[^&]+)', google_link)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error cleaning Google link: {e}")
        return None

# Scoring logic for ranking
def calculate_ranking_score(item, companies):
    score = 0

    # Source-based score
    if item.get("source") in TRUSTED_SOURCES:
        score += 40

    # Recency-based score
    if item.get("published"):
        try:
            published_date = datetime.strptime(item["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            time_diff = now - published_date
            if time_diff <= timedelta(hours=3):
                score += 25
            elif time_diff <= timedelta(hours=6):
                score += 15
            elif time_diff <= timedelta(hours=24):
                score += 5
        except Exception as e:
            print(f"Error parsing date for ranking: {e}")

    # Title-based keyword match
    if item.get("title"):
        title = item["title"].lower()
        if any(keyword.lower() in title for keyword in KEYWORDS):
            score += 25

    # Company mention-based score
    if item.get("title") or item.get("content"):
        text = (item.get("title", "") + " " + item.get("content", "")).lower()
        if any(company in text for company in companies):
            score += 20  # Add points for company mentions

    return score

# Function to extract and clean required fields
def filter_fields(data, companies, is_g_alerts=False):
    filtered_data = []
    for item in data:
        try:
            if is_g_alerts:
                link = item.get("cleaned_link") or clean_google_link(item.get("link", ""))
            else:
                link = item.get("link")

            if not link:
                print(f"Warning: Missing or invalid link for article titled '{item.get('title')}'")

            filtered_item = {
                "source": item.get("source"),
                "title": item.get("title"),
                "link": link,
                "published": item.get("published"),
                "content": item.get("content"),
                "summary": item.get("summary"),
            }
            # Add ranking score
            filtered_item["ranking_score"] = calculate_ranking_score(filtered_item, companies)
            filtered_data.append(filtered_item)
        except Exception as e:
            print(f"Error processing item: {e}")
    return filtered_data

# Function to remove articles mentioning Rwanda
def remove_articles_about_rwanda(data):
    return [
        item for item in data
        if "rwanda" not in (item.get("title", "").lower() + item.get("content", "").lower())
    ]

# Function to combine JSON files
def combine_json_files(file1, file2, company_list_file, output_file):
    try:
        # Load company names
        companies = load_company_list(company_list_file)

        # Read the first file (G_Alerts)
        with open(file1, "r", encoding="utf-8") as f1:
            data1 = json.load(f1)
            filtered_data1 = filter_fields(data1, companies, is_g_alerts=True)

        # Read the second file (Media Feeds)
        with open(file2, "r", encoding="utf-8") as f2:
            data2 = json.load(f2)
            filtered_data2 = filter_fields(data2, companies)

        # Merge the filtered data
        combined_data = filtered_data1 + filtered_data2

        # Remove articles mentioning Rwanda
        combined_data = remove_articles_about_rwanda(combined_data)

        # Sort by ranking score in descending order
        combined_data = sorted(combined_data, key=lambda x: x["ranking_score"], reverse=True)

        # Save to a new file
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(combined_data, out, indent=4, ensure_ascii=False)

        print(f"Combined JSON file saved as {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
combine_json_files(file1, file2, company_list_file, output_file)
