import csv
import pandas as pd
import scraper
from time import sleep

data_list = []
with open('data.csv', 'r') as file:
    df = pd.read_csv(file)
    website_column = df['Website']
    name_column = df["Name"]
    category = df['Category']
    for i in range(len(website_column)):
        if website_column[i] is not None:
            print("{} - ".format(i + 1), end="  ")
            orginal_url = website_column[i].replace('https://', '')
            orginal_url = orginal_url.strip('/')
            orginal_url = orginal_url.replace('www.', '')
            orginal_url = orginal_url.replace('http://', '')
            url = 'https://www.alexa.com/siteinfo/' + orginal_url
            # print(url)
            scraper.scrape_data(url, name_column[i], category, data_list)
        sleep(2)


csv_columns = ['Name', 'Website', 'Category', 'competitor 1', 'competitor 2', 'competitor 3', 'competitor 4',
               'competitor 5', 'Search Traffic (this site)', 'Search Traffic (comp.Avg', 'Bounce Rate (this site)',
               'Bounce Rate (comp.Avg', 'Site Linking in (this site)', 'Site Linking in (comp_avg)', 'alexa rank',
               'visitor country 1', 'visitor country 2', 'visitor country 3', 'visitor country 4',
               'Daily Pageviews per Visitor', 'Daily Time on Site', 'Bounce rate', 'visited before 1',
               'visited before 2', 'visited before 3', 'visited before 4', 'visited before 5', 'visited after 1',
               'visited after 2', 'visited after 3', 'visited after 4', 'visited after 5']

try:
    with open('test_csv.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)
except IOError:
    print("I/O error")

