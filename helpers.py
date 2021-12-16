from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def accept_cookies(browser, cookie_btn_xpath):
    """

    :param browser:
    :param cookie_btn_xpath:
    :return:
    """
    cookie_btn = browser.find_element(By.XPATH, cookie_btn_xpath)
    time.sleep(3)
    cookie_btn.click()
    print('Cookies accepted')


def edit_url(url_path, url_type='default', query=None, site=None):

    if url_type != 'default':
        query = f'site:{site}'+' '+ query
        query = str('+'.join(query.split()))
        url_path = 'https://google.com/search?q=' + query
        return url_path
    else:
        return url_path


def get_browser(url_path: str, open_browser=False, cookie_btn_xpath=None):
    """

    :param url_path:
    :param open_browser:
    :param cookie_btn_xpath:
    :return:
    """
    service = Service("./chromedriver")
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)

    if not open_browser:
        # Put following as part of config
        chr_options.add_argument('--headless')
        chr_options.add_argument('--no-sandbox')
        #chr_options.add_argument('--disable-dev-shm-usage')

    chrome_browser = webdriver.Chrome(service=service, options=chr_options)
    chrome_browser.maximize_window()

    chrome_browser.get(url_path)

    if cookie_btn_xpath is not None:
        accept_cookies(browser=chrome_browser, cookie_btn_xpath=cookie_btn_xpath)

    return chrome_browser


def make_search_click(browser, query: str, search_bar_xpath: str, btn_xpath=None, use_keys=False):

    search_bar = browser.find_element(By.XPATH, search_bar_xpath)
    search_bar.send_keys(query)
    if not use_keys:
        search_bar_btn = browser.find_element(By.XPATH, btn_xpath)
        search_bar_btn.click()
    else:
        search_bar.send_keys(Keys.RETURN)
