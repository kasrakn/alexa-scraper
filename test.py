import pandas as pd
import csv
import scraper
data= []
url = "https://www.alexa.com/siteinfo/facebook.com"
scraper.scrape_data(url, 'Social Media', 'Facebook', data)


