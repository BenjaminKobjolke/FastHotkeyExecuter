import requests
from bs4 import BeautifulSoup


class WebCrawler:
    soup: BeautifulSoup = None

    def __init__(self):
        pass

    def get_title(self):
        if self.soup is None:
            raise Exception("You need to call execute() first.")

        return self.soup.title.text

    def execute(self, url: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
        }

        response = requests.get(url, headers=headers)

        # step 2: parse HTML content
        self.soup = BeautifulSoup(response.content, 'html.parser')
        page_title = self.get_title()
        main_content = self.soup.find('main')

        if main_content:
            page_text = main_content.get_text(separator=' ')
        else:
            print("NO MAIN")
            page_text = self.soup.get_text(separator=' ')

        # truncate page_text to 1000 characters
        page_text = page_text[:20000]
        return_dict = {'title': page_title, 'text': page_text, 'tokens': 100, 'success': True}

        return return_dict
