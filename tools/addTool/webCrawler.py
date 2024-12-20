import requests
from bs4 import BeautifulSoup

def web_crawler(start_url):
    print(f"[*] Crawling {start_url}...")
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        print(f"[+] Found link: {link.get('href')}")