import requests
from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"} #ユーザエージェント設定
url = "https://ncode.syosetu.com/n7797gn/1/"
response = requests.get(url=url, headers=headers)
html = response.content
import re
soup = BeautifulSoup(html, "html.parser")
resultListing = ["p.novel_subtitle", "#novel_honbun"]
#print(soup.select_one(resultListing[0]).text)         #html形式[]
text = soup.select_one(resultListing[0]).text
print(text)
print(soup.select_one(resultListing[1]).text)
targetPage = soup.find('a', href=re.compile('..\/impression\/list\/..')).attrs['href']
print(targetPage)