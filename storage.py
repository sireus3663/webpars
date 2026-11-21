import requests
from bs4 import BeautifulSoup

class Storage:
    def __init__(self, url:str):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text,"html.parser")
        self.data = None
    def get_page(self, url:str):
        pass