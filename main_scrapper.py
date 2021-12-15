"""Scraper for articles """

# do a search on page
# check if there is something from this year
#  devide functions
# sort by date
# deliver by email

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from IPython.display import HTML


def do_search(url_path: str, queries: list, open_browser=False):

    n_pages = 1

    # ****** s1 create browser ******
    service = Service("./chromedriver")
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)

    if not open_browser:
        chr_options.add_argument('--headless') # part of class

    chrome_browser = webdriver.Chrome(service=service, options=chr_options)
    chrome_browser.maximize_window()
    chrome_browser.get(url_path)

    # ****** s2 do search ******

    df = pd.DataFrame()

    dates = []
    links = []

    for query in queries:

        print(f'Current query being processed: {query}')
        search_bar = chrome_browser.find_element(By.XPATH, '//*[@id="search-4"]/div/form/input[1]')
        search_bar.send_keys(query)
        search_bar_btn = chrome_browser.find_element(By.XPATH, '//*[@id="search-4"]/div/form/button')
        search_bar_btn.click()
        url_base = chrome_browser.current_url

        for i in range(0, n_pages):
            i = i + 1
            page_add = f'&paged={i}'
            current_url = url_base + page_add
            res = requests.get(current_url)

            if res.status_code == 403:
                print(f'There are no results for query:{query}')

            #print(f'Request status: {res.status_code}')
            soup = BeautifulSoup(res.text, 'html.parser')

            for row in soup.findAll('article'):
                date = pd.to_datetime(row.find('abbr', class_='date time published updated').text)
                dates.append(date)
                link = row.find('a').get('href')
                links.append(link)

    df['date'] = dates
    df['link'] = links
    #df['query'] = query
    print('sorting values..')
    df.sort_values('date', ascending=False, inplace=True)
    HTML(df.to_html(render_links=True, escape=False))
    # print(dates)
    # print(links)

    return df

urls = ['https://machinelearningmastery.com/start-here', ]
df = do_search(url_path='https://machinelearningmastery.com/start-here', queries=['MLOPS', 'lstm' , 'clv'], open_browser=False)
print(df)