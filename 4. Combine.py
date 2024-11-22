import json
from datetime import datetime, timezone, timedelta

# Input file paths
file1 = "9. G_Alerts_feed.json"
file2 = "9. Media_filtered_feeds.json"

# Output file path
output_file = "9. Combined_Feeds.json"

# Keywords to check in the title
KEYWORDS = ["real world assets", "real-world assets", "RWA", "Tokenisation", "Tokenization", "Tokenized"]

# Trusted sources
TRUSTED_SOURCES = ["Cointelegraph", "Coindesk", "Blockworks", "TechCrunch"]

# Function to parse dates with multiple formats
def parse_date(date_str):
    date_formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 (standard format)
        "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with microseconds
        "%a, %d %b %Y %H:%M:%S %z"  # RSS pubDate format
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    # Log the issue with unrecognized date formats
    print(f"Unrecognized date format: {date_str}")
    return None

# Scoring logic for ranking
def calculate_ranking_score(item):
    score = 0

    # Source-based score
    if item.get("source") in TRUSTED_SOURCES:
        score += 50

    # Recency-based score
    if item.get("published"):
        try:
            published_date = parse_date(item["published"])
            if published_date:
                now = datetime.now(timezone.utc)
                time_diff = now - published_date
                if time_diff <= timedelta(hours=3):
                    score += 30
                elif time_diff <= timedelta(hours=6):
                    score += 20
                elif time_diff <= timedelta(hours=24):
                    score += 10
        except Exception as e:
            print(f"Error parsing date for ranking: {e}")

    # Title-based keyword match
    if item.get("title"):
        title = item["title"].lower()
        if any(keyword.lower() in title for keyword in KEYWORDS):
            score += 15

    return score

# Function to extract only the required fields and calculate ranking score
def filter_fields(data, is_g_alerts=False):
    filtered_data = []
    for item in data:
        filtered_item = {
            "source": item.get("source"),
            "title": item.get("title"),
            "link": item.get("media_link") if is_g_alerts else item.get("link"),
            "published": item.get("published"),
            "content": item.get("content"),
            "summary": item.get("summary"),
        }
        # Add ranking score
        filtered_item["ranking_score"] = calculate_ranking_score(filtered_item)
        filtered_data.append(filtered_item)
    return filtered_data

# Function to combine JSON files
def combine_json_files(file1, file2, output_file):
    try:
        # Read the first file (G_Alerts)
        with open(file1, "r", encoding="utf-8") as f1:
            data1 = json.load(f1)
            filtered_data1 = filter_fields(data1, is_g_alerts=True)

        # Read the second file (Media)
        with open(file2, "r", encoding="utf-8") as f2:
            data2 = json.load(f2)
            filtered_data2 = filter_fields(data2)

        # Merge the filtered data
        combined_data = filtered_data1 + filtered_data2

        # Sort by ranking score in descending order
        combined_data = sorted(combined_data, key=lambda x: x["ranking_score"], reverse=True)

        # Save to a new file
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(combined_data, out, indent=4, ensure_ascii=False)

        print(f"Combined JSON file saved as {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
combine_json_files(file1, file2, output_file)
