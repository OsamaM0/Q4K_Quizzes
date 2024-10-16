from ..base_interface import IDocumentTextExtractor

from bs4 import BeautifulSoup
import requests
import random
import time


class HTMLExtractor(IDocumentTextExtractor):
    def __init__(self):
        self.scrapper = Scrapper()

    def extract_text(self, url: str) -> str:
        # Use the Scrapper class to get the text content from the web link
        soup = self.scrapper.get_response(url)
        return soup.get_text() if soup else "Failed to extract text from the web link."


class Scrapper:
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
    ]

    url_list = {}

    def send_request(self, url, proxies: list = None):
        headers = {'User-Agent': random.choice(self.user_agents)}
        try:
            if proxies is None:
                response = requests.get(url, headers=headers)
            else:
                response = requests.get(url, headers=headers, proxies=proxies)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            print("Exception in request:", e)
        return None

    def get_response(self, url):
        print("Starting Scraping")
        content = None
        url.strip()

        if url in self.url_list:
            print("Using cached content for URL")
            content = self.url_list[url]
        else:
            while not content:
                res = self.send_request(url)
                if res:
                    content = res.text
                    self.url_list[url] = content
                else:
                    time.sleep(random.uniform(1, 3))

        return BeautifulSoup(content, 'html.parser')
