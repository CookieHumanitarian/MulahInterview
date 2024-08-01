Design a Title Aggregator which scrapes Wired 

Required packages/extensions:
1. feedparser
2. pytz
3. Flask

Note:

I did not manage to scrape all the articles from Web Archive within the time limit
(I left it running for about 2 hours already), so below is my code for just scraping the articles from the RSS link from the websites itself

{import feedparser
from datetime import datetime
import pytz
import csv

#Get RSS of website
url = "https://www.wired.com/feed"
feed = feedparser.parse(url)

#Define range of dates
start_date = datetime(2022, 1, 1, tzinfo=pytz.UTC)
end_date = datetime.now(pytz.UTC)

#Convert feed date to datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        return None

#Prepare the CSV file
with open('rss_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'link', 'published']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    #Write the header row
    writer.writeheader()
    
    #Iterate through entries and write to the CSV file
    for entry in feed.entries:
        published_date = parse_date(entry.published)
        if published_date and start_date <= published_date <= end_date:
            writer.writerow({
                'title': entry.title,
                'link': entry.link,
                'published': published_date.strftime('%Y-%m-%d %H:%M:%S')
            })
