import requests
from bs4 import BeautifulSoup

class Parse:
    def __init__(self, url:str):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text,"html.parser")
        self.data = None
