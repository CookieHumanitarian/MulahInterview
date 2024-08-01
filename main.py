import feedparser
from datetime import datetime
import pytz  

# Get RSS of website
url = "https://www.wired.com/feed"
feed = feedparser.parse(url)

# Define range of dates
start_date = datetime(2022, 1, 1, tzinfo=pytz.UTC)
end_date = datetime.now(pytz.UTC)

# Convert feed date to datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        return None

# Check if there are any entries
for entry in feed.entries:
        published_date = parse_date(entry.published)
        if published_date and start_date <= published_date <= end_date:
            print(f"Title: {entry.title}")
            print(f"Link: {entry.link}")
            print(f"Published Date: {published_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print('-' * 40)
