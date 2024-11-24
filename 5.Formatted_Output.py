import json
import re

# Define a function to clean up the title
def clean_title(title):
    # Remove trailing ellipsis (...)
    title = title.strip().rstrip("...")
    # Remove "- Source Name" if it exists at the end
    title = re.sub(r" - \w+$", "", title)
    return title

# Define a function to reformat the date
def reformat_date(date):
    try:
        return date.replace("T", " ")[:-3]  # Removes seconds and replaces 'T' with a space
    except Exception as e:
        print(f"Error reformatting date '{date}': {e}")
        return date

# Define a function to deduplicate entries based on the 'link' field
def remove_duplicates(data):
    seen_links = set()
    unique_data = []
    for entry in data:
        link = entry.get('link', '')
        if link and link not in seen_links:  # Check if the link is already seen
            seen_links.add(link)
            unique_data.append(entry)
    return unique_data

# Load the combined JSON file
with open("9.Combined_Feeds.json", "r") as f:
    data = json.load(f)

# Process the data
cleaned_data = []
for entry in data:
    try:
        title = clean_title(entry.get('title', ''))
        source = entry.get('source', '')
        link = entry.get('link', '')
        published = reformat_date(entry.get('published', ''))

        # Append cleaned data
        cleaned_data.append({
            "source": source,
            "title": title,
            "link": link,
            "published": published
        })
    except Exception as e:
        print(f"Error processing entry: {e}")

# Remove duplicates
cleaned_data = remove_duplicates(cleaned_data)

# Save the final cleaned and deduplicated data
with open("9. Formatted_Feeds.json", "w") as f:
    json.dump(cleaned_data, f, indent=4)

print("Formatted and deduplicated data saved to '9. Formatted_Feeds.json'")
