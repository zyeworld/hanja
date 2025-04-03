# letter_*.json에 단어들을 채우기 위한 프로그램.
import requests
from bs4 import BeautifulSoup

# 싸지방에서 작동 안 돼서 실패
url = 'https://namu.wiki/w/%E6%9A%87'
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
else:
    print(response.status_code)