from bs4 import BeautifulSoup
import requests

#url로 부터 soup 파싱
def get_soup(url):
    result = requests.get(url)
    #print(result.status_code)
    soup = BeautifulSoup(result.text, "html.parser")

    return soup

