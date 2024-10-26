from ..base_interface import IDocumentTextExtractor
from bs4 import BeautifulSoup
import aiohttp
import random
import asyncio
import requests
import time


class HTMLExtractor(IDocumentTextExtractor):
    def __init__(self):
        self.scrapper = Scrapper()

    async def extract_text(self, url: str) -> str:
        # Use the Scrapper class to get the text content from the web link
        soup = await self.scrapper.get_response(url)
        return soup if soup else "Failed to extract text from the web link."


class Scrapper:

  # Define the URL and headers to use for the request
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  }

  # Define a list of user agent strings to use for the request
  user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
  ]

  # Send a request with a random proxy and user agent
  async def send_request(self, url, proxyes: list = None):
    # Pick Random Proxy & User_agent
    #proxy = random.choice(proxyes)
    headers = {'User-Agent': random.choice(self.user_agents)}

    # Get HTML of Desierd Url
    try:
      if proxyes is None:
        response = requests.get(url, headers=headers)
      else:
        response = requests.get(url, headers=headers, proxies=proxyes)
      if response.status_code == 200:
        print(response)
        return response

    except requests.exceptions.RequestException as e:
      print("Exception in requist  ", e)
    except:
      return None

  async def get_response(self, url):

    content = None
    url.strip()

    while not content:
      res = await self.send_request(url)
      if not res:
        # Wait for a random amount of time before trying again
        time.sleep(random.uniform(1, 3))
      else:
        content = res.text
      print("Try")

    return content