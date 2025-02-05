from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, Comment
import time

from import_hotkeys.data.config_loader import ConfigLoader
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils
from import_hotkeys.web.WebCrawler import WebCrawler


class ChromeWebCrawler(WebCrawler):
    wait_limit = 10
    min_html_length = 1000
    min_string_length = 300
    driver = None
    driver_path: str = None
    soup: BeautifulSoup = None

    def __init__(self, driver_path=None):
        super().__init__()
        self.driver_path = driver_path
        # Set base path for FileUtils
        FileUtils.set_base_path(str(Path(__file__).parent.parent.parent.parent))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the Chrome driver if it exists."""
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")
            finally:
                self.driver = None

    def get_title(self):
        if self.soup is None:
            raise Exception("You need to call execute() first.")

        if self.soup.title is None:
            return ""
        return self.soup.title.text

    def setup_driver(self, force=False):
        if force is False:
            if self.driver is not None:
                return
        
        options = Options()
        config = ConfigLoader()

        # Add extensions if configured
        extension_1 = config.get_setting('chromium', 'extension_1')
        if extension_1:
            extension_1_path = FileUtils.chrome_extension_path(extension_1)
            print("Loading extension: " + extension_1_path)
            options.add_extension(extension_1_path)

        extension_2 = config.get_setting('chromium', 'extension_2')
        if extension_2:
            extension_2_path = FileUtils.chrome_extension_path(extension_2)
            print("Loading extension: " + extension_2_path)
            options.add_extension(extension_2_path)

        # options.add_argument("--headless")
        options.add_argument("--window-size=1024,720")

        # Add proxy if configured
        use_proxy = config.get_setting('proxy', 'use_proxy', False)
        if use_proxy:
            protocol = config.get_setting('proxy', 'protocol')
            url = config.get_setting('proxy', 'url')
            user = config.get_setting('proxy', 'user')
            password = config.get_setting('proxy', 'password')
            proxy = protocol + "://" + user + ":" + password + "@" + url
            options.add_argument(f'--proxy-server={proxy}')

        # Initialize driver with or without custom path
        if self.driver_path:
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(options=options, service=service)
        else:
            self.driver = webdriver.Chrome(options=options)

    def execute(self, url: str):

        self.setup_driver()

        try:
            self.driver.get(url)
        except Exception as e:
            print("Failed to load page: " + str(e))
            print("Trying to load driver")
            self.setup_driver()
            try:
                self.driver.get(url, True)
            except Exception as e:
                print("Failed to load page again: " + str(e))
                self.close()
                return {'title': '', 'text': '', 'tokens': 0, 'success': False}

        # time.sleep(5)
        return self.wait_for_html()

    def wait_for_html(self, wait_counter=0):
        # waiting for popup and cookies addons to finish
        time.sleep(3)

        html = self.driver.find_element(By.CSS_SELECTOR, "html").get_attribute('innerHTML')
        self.soup = BeautifulSoup(html, 'html.parser')

        for tag in self.soup(['script', 'style', 'iframe', 'noscript']):
            tag.extract()

        for tag in self.soup(text=lambda text: isinstance(text, Comment)):
            tag.extract()

        for tag in self.soup.find_all():
            if tag.text == "":
                tag.extract()
                continue

            for key in dict(tag.attrs):
                del tag.attrs[key]

        page_text = None

        if self.soup.find(name="main"):
            #p rint("Found main")
            page_text = str(self.soup.find(name="main"))

            if self.soup.find(name="body"):
                # print("Found body")
                page_text_string = StringUtils.strip_html_tags(page_text)
                body_text = str(self.soup.find(name="body"))
                body_text_string = StringUtils.strip_html_tags(body_text)
                length_page_text_string = len(page_text_string)
                length_body_text_string = len(body_text_string)
                #p rint("Length page text string: " + str(length_page_text_string))
                #p rint("Length body text string: " + str(length_body_text_string))
            if length_page_text_string < self.min_string_length and length_body_text_string > length_page_text_string:
                page_text = body_text
        elif self.soup.find(name="body"):
            page_text = str(self.soup.find(name="body"))

        print("Page text length: " + str(len(page_text)))
        if page_text is None or len(page_text) < self.min_html_length:
            print("No body found!")
            if wait_counter < self.wait_limit:
                print("No html found, waiting 1 second")
                time.sleep(1)
                wait_counter += 1
                return self.wait_for_html(wait_counter)
            else:
                result = {'title': self.get_title(), 'text': page_text, 'tokens': 100, 'success': False}
                self.close()
                return result
                
        result = {'title': self.get_title(), 'text': page_text, 'tokens': 100, 'success': True}
        self.close()
        return result
