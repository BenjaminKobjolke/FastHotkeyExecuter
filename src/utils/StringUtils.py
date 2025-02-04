import html2text
import pycountry
from bs4 import BeautifulSoup
import re
from langdetect import detect


class StringUtils:
    @staticmethod
    def contains_html(string):
        soup = BeautifulSoup(string, 'html.parser')
        if soup.find():
            return True
        else:
            return False

    @staticmethod
    def strip_html_tags(html_string):
        soup = BeautifulSoup(html_string, "html.parser")
        stripped_string = soup.get_text(separator=" ")
        return stripped_string

    @staticmethod
    def trim_string(input_string, length):
        trimmed_string = input_string[:length]
        trimmed_string = re.sub(r'\s+', ' ', trimmed_string)
        # remove erroneous whitespace
        return trimmed_string.strip()

    @staticmethod
    def convert_html_to_markdown(html_text):
        h = html2text.HTML2Text()
        # Ignore converting links from HTML into URL footnotes.
        h.ignore_links = False
        return h.handle(html_text)

    @staticmethod
    def detect_language(text, default="en"):
        # if length text < 1
        if len(text) < 1:
            return "unknown"
        try:
            lang = detect(text)
        except Exception as e:
            print(f"An error occurred: {e}")
            lang = default
        #p rint(f"Detected language: {lang}")
        return lang

    @staticmethod
    def convert_language_code(lang):
        try:
            language = pycountry.languages.get(alpha_2=lang)
            return language.alpha_3
        except Exception as e:
            print(f"Error: {e}")
            return lang  # return original code if not found
