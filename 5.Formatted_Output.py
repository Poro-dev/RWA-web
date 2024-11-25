import json
from datetime import datetime, timezone, timedelta
import re

def normalize_text(text):
    """Normalize text by converting to lowercase and stripping whitespace."""
    return text.lower().strip() if text else ""

def clean_title(title, source):
    """Cleans up the title by removing the repeated source after a hyphen."""
    if not title or not source:
        return title
    # Normalize title and source for consistent comparison
    normalized_source = normalize_text(source)
    title_parts = title.split(" - ")

    # Check if any part of the title matches the normalized source
    if len(title_parts) > 1 and normalize_text(title_parts[-1]) == normalized_source:
        return " - ".join(title_parts[:-1])  # Remove the last part if it matches the source
    return title

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

def format_date(date_str):
    """Formats the date into a more readable format."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")  # Fix datetime string parsing
        return date_obj.strftime("%d-%b-%y %H:%M")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")  # Handle millisecond timestamps
            return date_obj.strftime("%d-%b-%y %H:%M")
        except ValueError:
            return date_str  # Return the original date string if parsing fails

def process_data(data):
    unique_titles = {}
    for item in data:
        # Clean title and remove repeated source
        item["title"] = clean_title(clean_text(item.get("title")), item.get("source"))
        # Format the date
        item["published"] = format_date(item.get("published"))
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

