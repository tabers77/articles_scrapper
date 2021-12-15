"""Google scraper:
 Info: https://support.google.com/websearch/answer/2466433?hl=en
 https://cleverclicksdigital.com/blog/15-awesome-google-search-tricks/
 """
# make search of a certain page by date

import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from IPython.display import HTML
from helpers import *

chrome_browser = get_activate_browser(url_path='https://www.google.com/', open_browser=True, cookie_btn_xpath='//*[@id="L2AGLb"]')

make_search_click(browser=chrome_browser, query='test', search_bar_xpath='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input', use_keys=True )

