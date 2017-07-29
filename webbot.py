import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class WebBot:
    def __init__(self, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}):
        self.session = requests.session()
        self.response = None
        self.soup = None
        self.url = None
        self.driver = None
        self.headers = headers

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.driver:
            self.driver.close()

    def close(self):
        self.__exit__(None, None, None)

    def __clear(self):
        self.response = None
        self.soup = None
        self.url = None

    def __split_url(self):
        try:
            protocol_index = self.url.index("//") + 2
        except ValueError:
            protocol_index = 0

        protocol = self.url[:protocol_index]

        domain_index = self.url.index("/", len(protocol)) + 1
        domain = self.url[protocol_index:domain_index]

        rest = self.url[domain_index:]
        return protocol, domain, rest

    def __get_domain(self):
        return self.__split_url()[1]

    def __get(self):
        return self.session.get(self.url, headers=self.headers)

    def driver_connect(self):
        if not self.driver:
            self.driver = webdriver.Firefox()

        self.driver.get(self.url)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))

    def connect(self, url, driver=False):
        self.__clear()

        try:
            self.url = url
            self.response = self.__get()

            if driver:
                self.driver_connect()
            return self.response
        except requests.exceptions.MissingSchema:
            pass

        try:
            protocol, domain, rest = self.__split_url()
            self.url = "http://" + domain + rest
            self.response = self.__get()

            if driver:
                self.driver_connect()
            return self.response
        except requests.exceptions.MissingSchema:
            pass

        protocol, domain, rest = self.__split_url()
        self.url = "https://" + domain + rest
        self.response = self.__get()

        if driver:
            self.driver_connect()

        return self.response

    def get_response_content(self, url=None):
        if url:
            self.connect(url)
            return self.get_response_content()

        if self.response:
            return self.response.text

    def get_soup(self, url=None, parser='html5lib'):
        if self.driver:
            if self.driver:
                page_source = self.driver.page_source
                self.soup = BeautifulSoup(page_source, "html5lib")
                return self.soup

        self.soup = BeautifulSoup(self.get_response_content(url), parser)
        return self.soup

    def get_content(self):
        if not self.soup:
            self.get_soup()

        return self.soup.prettify()

    def exec(self, method, *list, **kwargs):
        url = kwargs.get('url', None)
        self.get_soup(url)

        method = getattr(self.soup, method)
        return method(*list, **kwargs)

    def click(self, index=0, driver=False, **kwargs):
        if not self.soup:
            self.get_soup()

        links = self.soup.find_all('a', **kwargs)
        link = links[index].get('href')

        domain = self.__get_domain()
        if not link.startswith("http://") and not link.startswith("https://") and \
                not link.startswith("www.") and not link.startswith(self.__get_domain()):
            return self.connect(domain + link)

        return self.connect(link, driver)

    def __find_element(self, tag, path="", args={}):
        def key_wrapper(key):
            if key == "text":
                return "text()"
            return "@" + key

        xpath = "{}//{}{}".format(
            path,
            tag,
            "" if len(args) == 0
            else "[{}]".format(
                ",".join([
                    "{}='{}'".format(
                        key_wrapper(key), value
                    )
                    for key, value
                    in args.items()
                ])
            )
        )

        print(xpath)

        return self.driver.find_element_by_xpath(xpath)

    def search(self, input_text, path="", submit=False, args={}):
        if not self.driver:
            self.driver = webdriver.Firefox()

        self.driver.get(self.url)

        search = self.__find_element("input", path, args)
        search.send_keys(input_text)
        if submit:
            search.submit()

        try:
           WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))
        except TimeoutException:
            print("Loading took too much time!")

    def wait(self, sleep_time=0, driver_time=5, tag=None, path="", args={}):
        time.sleep(sleep_time)

        if tag:
            WebDriverWait(self.driver, driver_time).until(
                lambda x: self.__find_element(tag, path, args)
            )



