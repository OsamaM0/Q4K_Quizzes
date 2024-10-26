from ..base_interface import IDocumentTextExtractor
from bs4 import BeautifulSoup
import aiohttp
import random
import asyncio


class HTMLExtractor(IDocumentTextExtractor):
    def __init__(self):
        self.scrapper = Scrapper()

    async def extract_text(self, url: str) -> str:
        # Use the Scrapper class to get the text content from the web link
        soup = await self.scrapper.get_response(url)
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

    async def send_request(self, url, proxies: list = None):
        headers = {'User-Agent': random.choice(self.user_agents)}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    print(f"Status Code: {response.status}, URL: {url}")
                    content = await response.text()
                    print(f"Content Length: {len(content)}")  # Log the length of the content
                    if response.status == 200:
                        return content
            except aiohttp.ClientError as e:
                print("Exception in request:", e)
        return None


    async def get_response(self, url):
        print("Starting Scraping")
        content = None
        url.strip()

        if url in self.url_list:
            print("Using cached content for URL")
            content = self.url_list[url]
        else:
            while not content:
                res = await self.send_request(url)
                if res:
                    content = res
                    self.url_list[url] = content
                else:
                    await asyncio.sleep(random.uniform(1, 3))  # Proper async sleep

        return BeautifulSoup(content, 'html.parser')
