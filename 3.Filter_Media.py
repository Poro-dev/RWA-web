import json
import re
from datetime import datetime

# Keywords to filter articles (case-insensitive)
keywords = [
    "real world assets",
    "real-world assets",
    "RWA",
    "Tokenisation",
    "Tokenization",
    "Tokenized"
]

# Function to check and convert date format
def convert_date_format(date_string):
    try:
        # Attempt to parse as ISO 8601 format first
        if "T" in date_string and "Z" in date_string:
            return date_string  # Already in ISO 8601 format
    except ValueError:
        pass  # Continue to attempt parsing in other formats

    try:
        # Parse and convert the date from the alternate format
        parsed_date = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        print(f"Error converting date format for: {date_string}, Error: {e}")
        return date_string  # Return the original date if conversion fails

# Function to filter articles based on keywords
def filter_articles(articles, keywords):
    filtered = []
    keyword_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(k) for k in keywords) + r')\b', re.IGNORECASE)

    for article in articles:
        # Combine title, summary, content, and categories for keyword matching
        content_to_search = (
            f"{article['title']} {article['summary']} {article['content']} {' '.join(article.get('categories', []))}".lower()
        )

        # Check for keyword match using regex
        if keyword_pattern.search(content_to_search):
            filtered.append(article)

    return filtered

# Main function to filter and update articles
def main():
    # Load the consolidated JSON
    with open("9.Media_consolidated_feeds.json", "r", encoding="utf-8") as f:
        all_articles = json.load(f)

    print(f"Loaded {len(all_articles)} articles. Filtering...")

    # Filter the articles based on keywords
    filtered_articles = filter_articles(all_articles, keywords)
    print(f"Filtered down to {len(filtered_articles)} articles.")

    # Apply date format conversion to filtered articles
    for article in filtered_articles:
        if "published" in article:
            converted_date = convert_date_format(article["published"])
            article["published"] = converted_date

    # Save the filtered and updated articles to a new JSON file
    with open("9.Media_filtered_feeds.json", "w", encoding="utf-8") as f:
        json.dump(filtered_articles, f, indent=4)
    print("Filtered and updated articles saved to 9.Media_filtered_feeds.json.")

# Entry point for the script
if __name__ == "__main__":
    main()
