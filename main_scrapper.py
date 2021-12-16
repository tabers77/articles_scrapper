"""Scraper for articles """
import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import HTML
from helpers import *


def main_scraper(url_path: str, queries: list, n_pages=1, open_browser=False):

    chrome_browser = get_activate_browser(url_path=url_path, open_browser=open_browser)
    # ****** s2 do search ******

    df = pd.DataFrame()

    dates = []
    links = []
    query_list = []
    #status = 0
    for query in queries:

        print(f'Current query being processed: {query}')

        make_search_click(browser=chrome_browser, query=query, search_bar_xpath='//*[@id="search-4"]/div/form/input[1]',
                          btn_xpath='//*[@id="search-4"]/div/form/button')
        url_base = chrome_browser.current_url

        for i in range(0, n_pages):
            i = i + 1
            page_add = f'&paged={i}'
            current_url = url_base + page_add
            res = requests.get(current_url)

            #if res.status_code == 403:
             #   status += 1

            soup = BeautifulSoup(res.text, 'html.parser')
            for row in soup.findAll('article'):
                date = pd.to_datetime(row.find('abbr', class_='date time published updated').text)
                dates.append(date)
                link = row.find('a').get('href')
                links.append(link)
                query_list.append(f'tag:{query}')

    df['query'] = query_list
    df['date'] = dates
    df['link'] = links

    df.sort_values('date', ascending=False, inplace=True)
    HTML(df.to_html(render_links=True, escape=False))

    return df


urls = ['https://machinelearningmastery.com/start-here']
queries = ['logistic regression', 'keras']

df_samp = main_scraper(url_path='https://machinelearningmastery.com/start-here', queries=queries,
                       open_browser=False)
print(df_samp)