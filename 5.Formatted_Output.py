import json
import re
from datetime import datetime

# Input file (combined JSON)
input_file = "9. Combined_Feeds.json"
# Output file (formatted JSON)
output_file = "9. Formatted_Feeds.json"

# Function to reformat dates to 'YYYY-MM-DD HH:MM'
def reformat_date(date_str):
    try:
        # Parse the original date
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Format to 'YYYY-MM-DD HH:MM'
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        try:
            # Try the format without milliseconds
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"Error reformatting date '{date_str}': {e}")
            return date_str  # Return the original date if formatting fails

# Function to clean text (remove HTML tags and encoded characters)
def clean_text(text):
    if not isinstance(text, str):
        return text  # Skip cleaning if it's not a string
    try:
        # Remove HTML tags using regex
        clean = re.sub(r"<[^>]+>", "", text)
        # Decode HTML entities like &#39;
        clean = re.sub(r"&#39;", "'", clean)
        clean = re.sub(r"&amp;", "&", clean)
        clean = re.sub(r"&quot;", '"', clean)
        clean = re.sub(r"&lt;", "<", clean)
        clean = re.sub(r"&gt;", ">", clean)
        return clean.strip()
    except Exception as e:
        print(f"Error cleaning text '{text}': {e}")
        return text  # Return the original text if cleaning fails

# Main formatting function
def format_json(input_file, output_file):
    try:
        # Load the combined JSON data
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Format each entry
        for entry in data:
            if "published" in entry:
                entry["published"] = reformat_date(entry["published"])
            if "title" in entry:
                entry["title"] = clean_text(entry["title"])
            if "summary" in entry:
                entry["summary"] = clean_text(entry["summary"])

        # Save the formatted data to a new JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Formatted JSON file saved as {output_file}")

    except Exception as e:
        print(f"Error: {e}")

# Run the script
if __name__ == "__main__":
    format_json(input_file, output_file)
