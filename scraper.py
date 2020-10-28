from lxml.html import fromstring, tostring
from crawler.advanced_link_crawler import download
# from chp3.advanced_link_crawler import Downloader
from bs4 import BeautifulSoup
import html5lib


def scrape_data(url, name,category, data_list):
    d = dict()
    html = download(url)
    d['Name'] = name
    d['Website'] = url
    d['Category'] = category
    tree = fromstring(html)

    try:
        competitors = tree.xpath('//div[@class="Body"]//div[@class="Row"]/div[@class="site "]/a[@class="truncation"]/text()')[4:9]
        for ind, val in enumerate(competitors):
            d['competitor {}'.format(ind + 1)] = competitors[ind]
    except:
        d['competitor 1'] = None

    try:
        # comparison_metrics1 = tree.xpath('//div[contains(@class, "flex") and contains(@class, "maginbottom20")]//span[contains(@class, "purple")]/text()')
        # comparison_metrics1 = tree.xpath('//div[contains(@class, "flex") and contains(@class, "maginbottom20")]//div[contains(@class, "bignsquare")]/style  ')
        # print(comparison_metrics1)
        search_traffic_this = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[1]/div[2]/span/text()')
        if len(search_traffic_this) == 0:
            d['Search Traffic (this site)'] = None
        else:
            d['Search Traffic (this site)'] = search_traffic_this[0]
    except :
        d['Search Traffic (this site)'] = None


    try:
        search_traffic_comp = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[2]/div[2]/span/text()')
        if len(search_traffic_comp) == 0 or search_traffic_comp[0] == ' ':
            d['Search Traffic (comp.Avg'] = None
        else:
            d['Search Traffic (comp.Avg'] = search_traffic_comp[0]
    except:
        d['Search Traffic (comp.Avg'] = None

    try:
        bounce_rate_this = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[3]/div[2]/span/text()')
        if len(bounce_rate_this) == 0:
            d['Bounce Rate (this site)'] = None
        else:
            d['Bounce Rate (this site)'] = bounce_rate_this[0]
    except:
        d['Bounce Rate (this site)'] = None
    try:
        bounce_rate_comp = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[4]/div[2]/span/text()')
        if len(bounce_rate_comp) == 0 or bounce_rate_comp[0] == ' ':
            d['Bounce Rate (comp.Avg'] = None
        else:
            d['Bounce Rate (comp.Avg'] = bounce_rate_comp[0]
    except:
        d['Bounce Rate (comp.Avg'] = None

    try:
        site_linking_this = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[5]/div[2]/span/text()')[0]
        if site_linking_this == 0:
            d['Site Linking in (this site)'] = None
        else:
            d['Site Linking in (this site)'] = site_linking_this[0]
    except:
        d['Site Linking in (this site)'] = None

    try:
        site_linking_comp = tree.xpath('//*[@id="card_mini_competitors"]/section[2]/div[6]/div[2]/span/text()')[0]
        if site_linking_comp == 0:
            d['Site Linking in (comp_avg)'] = None
        else:
            d['Site Linking in (comp_avg)'] = site_linking_comp[0]
    except:
        d['Site Linking in (comp_avg)'] = None

    try:
        d['alexa rank'] = int(tree.xpath('//div[@class="rank-global"]/div//p[contains(@class, "big") and contains(@class, "data")]/text()')[1].strip('\n\t\t\t\t\t\t\t\t\t      \t        ').replace(",", ""))
    except:
        d['alexa rank'] = None

    try:
        countries = tree.xpath('//div[@class="visitorList"]/ul/li/div[@id="countryName"]/text()')
        countryPer = tree.xpath('//div[@class="visitorList"]/ul/li/div[@id="countryPercent"]/text()')
        for ind, country in enumerate(countries):
            country = country.strip()
            d['visitor country {}'.format(ind + 1)] = country.replace('\xa0', '') + "({})".format(countryPer[ind])
    except:
        d['visitor country 1'] = None

    try:
        engagment = tree.xpath('//section[@class="engagement"]/div[@class="flex"]/div[contains(@class, "sectional")]/p[contains(@class, "small")]/text()')
    except:
        engagment = None

    try:
        daily_pagevies = tree.xpath('//*[@id="card_metrics"]/section[2]/div[2]/div[1]/p[1]/text()')
        d['Daily Pageviews per Visitor'] = daily_pagevies[0].strip('\n\t\t\t\t\t\t\t\t\t      \t            ')
        # d['Daily Pageviews per Visitor'] = engagment[0].strip("\n\t\t\t\t\t\t\t\t\t      \t            ")
    except:
        d['Daily Pageviews per Visitor'] = None

    try:
        # d['Daily Time on Site'] = engagment[2].strip("\n\t\t\t\t\t\t\t\t\t      \t            ")
        daily_time_on_site = tree.xpath('//*[@id="card_metrics"]/section[2]/div[2]/div[2]/p/text()')
        # d['Daily Time on Site'] = engagment[2]
        d['Daily Time on Site'] = daily_time_on_site[0].strip('\n\t\t\t\t\t\t\t\t\t      \t            ')
    except:
        d['Daily Time on Site'] = None

    try:
        bounce_rate = tree.xpath('//*[@id="card_metrics"]/section[2]/div[2]/div[3]/p/text()')
        d['Bounce rate'] = bounce_rate[0].strip('\n\t\t\t\t\t\t\t\t\t      \t            ')
        # d['Bounce rate'] = engagment[4].strip("\n\t\t\t\t\t\t\t\t\t      \t            ")
    except:
        d['Bounce rate'] = None

    try:
        site_flow_per = tree.xpath('//section[@class="stream"]/div[@class="flex"]/div/p/span/text()')
        site_flow = tree.xpath('//section[@class="stream"]/div[@class="flex"]/div/p/text()')
        visited_before = site_flow[:5]
        visited_before_per = site_flow_per[:5]
        visited_after = site_flow[5:]
        visited_after_per = site_flow[5:]
        for ind, val in enumerate(visited_before):
            d['visited before {}'.format(ind + 1)] = visited_before[ind] + "({})".format(visited_before_per[ind])
        for ind, val in enumerate(visited_after):
            d['visited after {}'.format(ind + 1)] = visited_after[ind] + "({})".format(visited_after_per[ind])

    except:
        d['visited before 1'] = None
        d['visited after 1'] = None

    data_list.append(d)
    with open('./data/{}.txt'.format(name), 'w') as outputfile:
        outputfile.write(d.items().__str__())

