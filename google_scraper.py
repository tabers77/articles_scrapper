"""Google scraper:
 Info: https://support.google.com/websearch/answer/2466433?hl=en
 https://cleverclicksdigital.com/blog/15-awesome-google-search-tricks/
 """
#

from bs4 import BeautifulSoup
from helpers import *
import pandas as pd
pd.set_option('display.max_colwidth', None) # add to EDA exercises
import dateparser# add to EDA exercises date parser for non english

import numpy as np

base_sites = ['machinelearningmastery.com', 'towardsdatascience.com', 'analyticsvidhya.com']

general_dict = {}

for site in base_sites:
    print(site)
    url = edit_url(url_path='https://www.google.com/', url_type='google', query='clv', site=site)

    n_pages = 2

    for page in range(n_pages):

        current_url = url + "&start=" + str(page)
        print(f'current url:{current_url}')
        time.sleep(3)
        driver = get_browser(url_path=current_url, open_browser=False)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for row in soup.find_all('div', class_="g"):

            try:
                published_date = str(row.find('span', class_='MUxGbd wuQ4Ob WZ8Tjf').text).replace('.', '').replace('—',
                                                                                                                 '')
                published_date = dateparser.parse(published_date)

            except AttributeError as err:
                published_date = np.nan

            title = row.find('h3').text
            link = row.a.get('href')
            general_dict.setdefault('published_date', []).append(published_date)
            general_dict.setdefault('site', []).append(site)
            general_dict.setdefault('title', []).append(title)
            general_dict.setdefault('link', []).append(link)


df = pd.DataFrame(general_dict).sort_values('published_date', ascending=False).reset_index(drop=True)  # add to EDA exercises

print(df)

