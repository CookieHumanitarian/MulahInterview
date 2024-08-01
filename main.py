import requests
import feedparser
from datetime import datetime
import pytz  
import csv
import json
import time

# Function to fetch and parse RSS feed from a given URL
def fetch_feed(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return feedparser.parse(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching feed from {url}: {e}")
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
    return None

# Function to process and collect feed entries within a specified date range
def collect_feed_entries(feed, start_date, end_date, collected_entries):
    for entry in feed.entries:
        published_date = entry.get('published_parsed')
        if published_date:
            published_date = datetime(*published_date[:6], tzinfo=pytz.UTC)
            if start_date <= published_date <= end_date:
                collected_entries.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': published_date.strftime('%Y-%m-%d %H:%M:%S')
                })

# Function to fetch URLs from Wayback Machine for a given site and date range
def fetch_wayback_urls(base_url, start_date, end_date):
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')
    
    api_url = (
        f"http://web.archive.org/cdx/search/cdx?"
        f"url={base_url}*&from={start_date_str}&to={end_date_str}"
        f"&output=json&fl=timestamp,original&limit=10000"
    )
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = json.loads(response.text)
        return data[1:]  # Skip the header row
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from Wayback Machine: {e}")
        return []

# Define date range
start_date = datetime(2022, 1, 1, tzinfo=pytz.UTC)
end_date = datetime.now(pytz.UTC)

# Base URL of the site for Wayback Machine
base_url = "www.wired.com"

# Fetch URLs from Wayback Machine
wayback_urls = fetch_wayback_urls(base_url, start_date, end_date)

# Collect feed entries from Wayback Machine URLs
collected_entries = []

for timestamp, original_url in wayback_urls:
    wayback_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
    print(f"Processing feed from: {wayback_url}")
    feed = fetch_feed(wayback_url)
    if feed:
        collect_feed_entries(feed, start_date, end_date, collected_entries)

# Prepare the CSV file
with open('rss_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'link', 'published']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # Write collected entries to the CSV file
    for entry in collected_entries:
        writer.writerow(entry)

print("Data collection complete. Check rss_data.csv for results.")
