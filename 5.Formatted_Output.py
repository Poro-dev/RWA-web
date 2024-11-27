import json
from datetime import datetime, timezone, timedelta
import re

def normalize_text(text):
    """Normalize text by converting to lowercase and stripping whitespace."""
    return text.lower().strip() if text else ""

def clean_title(title, source):
    """Cleans up the title by removing unnecessary parts."""
    if not title:
        return title

    # Remove everything after " - "
    if " - " in title:
        title = title.split(" - ")[0]

    # Remove everything after "|"
    if "|" in title:
        title = title.split("|")[0]

    # Clean repeated source if present
    if source:
        normalized_source = normalize_text(source)
        title_parts = title.split(" - ")
        if len(title_parts) > 1 and normalize_text(title_parts[-1]) == normalized_source:
            title = " - ".join(title_parts[:-1])  # Remove the last part if it matches the source

    return title.strip()  # Ensure there’s no trailing whitespace

def clean_text(text):
    """Removes HTML tags and decodes HTML entities."""
    if not text:
        return text
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = text.replace("&#39;", "'")
    text = text.replace("&quot;", '"')
    text = text.replace("&amp;", "&")
    return text

def relative_time(date_str):
    """Converts a timestamp into a relative time string with emojis."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - date_obj

        # Convert time delta into a human-readable string with emojis
        if delta < timedelta(hours=1):
            return f"⚡ Just now"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            days = delta.days
            return f"{days}d ago"
    except ValueError:
        return "unknown time"

def process_data(data):
    unique_titles = {}
    for item in data:
        # Clean title and remove repeated source
        item["title"] = clean_title(clean_text(item.get("title")), item.get("source"))
        # Convert published date to relative time with emojis
        item["published"] = relative_time(item.get("published"))
        # Create a unique identifier for each entry based on title and source
        key = (item["title"], item.get("source"))

        # Only add the item if the title has not been added before
        if key not in unique_titles:
            unique_titles[key] = item

    # Return only the values from the dictionary, which will be a list of unique items
    return list(unique_titles.values())

# Load JSON data from the input file
input_file = "9.Combined_Feeds.json"
output_file = "9.Formatted_Feeds.json"

with open(input_file, "r") as infile:
    data = json.load(infile)

# Process the data
formatted_data = process_data(data)

# Save the formatted data back to a new JSON file
with open(output_file, "w") as outfile:
    json.dump(formatted_data, outfile, indent=4)
