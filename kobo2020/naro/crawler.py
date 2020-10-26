import re
import requests
from bs4 import BeautifulSoup
import time
class Website:
    def __init__(self, url, targetPattern, commentTag, bodyTag, errorTags):
        self.url = url
        self.targetPattern = targetPattern
        self.commentTag = commentTag
        self.bodyTag = bodyTag
        self.errorTags = errorTags

class Content:
    def __init__(self):
        self.comments = []
        self.body = []
    
    def printing(self):
        print(len(self.comments)-len(self.body))
        print(len(self.body))

    def setContent(self, comments, body):
        self.comments.extend([comment.replace('\n', '') for comment in comments])
        self.comments.append('[END]')
        self.body.append(body[0].replace('\n', ''))
        print(body[0].replace('\n', ''))
        print([comment.replace('\n', '') for comment in comments])
    
    def save(self, commentPath, bodyPath):
        with open(commentPath, mode="w", encoding='utf-8') as f:
            f.write('\n'.join(self.comments))
        with open(bodyPath, mode="w", encoding='utf-8') as f:
            f.write('\n'.join(self.body))


class Crawler:
    def __init__(self, site, headers, contentObj):
        self.site = site
        self.visited = []
        self.headers = headers
        self.content = contentObj

    def getPage(self, url):
        try:
            req = requests.get(url=url, headers = self.headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return [elem.get_text() for elem in selectedElems]
        return None

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            impressionPage = bs.find('a', href=re.compile(self.site.targetPattern)).attrs['href']
            bsi = self.getPage(impressionPage)
            comments = self.safeGet(bsi, self.site.commentTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if comments != None and body != None:
                self.content.setContent(comments, body)
        
    def crawl(self):
        if self.site.url not in self.visited:
           self.visited.append(self.site.url)
        else:return
        i = 1
        bs = self.getPage(self.site.url)
        if bs is None:
            print("bs is None!")
            return
        impressionPage = bs.find('a', href=re.compile(self.site.targetPattern)).attrs['href']
        bsi = self.getPage(impressionPage)
        if bsi.select_one('div.nothing') is not None:
            print("impression does not exist!")
            return
        while True:
            targetPage = "{}{}".format(self.site.url, i)
            bs = self.getPage(targetPage)
            if bs.html.head.title.text =="エラー":
                print("break!!")
                break
            # if bs.select_one(self.site.errorTags[0]).select_one(self.site.errorTags[1]) is not None:
            #     break
            self.parse(targetPage)
            self.content.save("commet.txt", "body.txt")
            time.sleep(2)
            i += 1
        
def searchRankingUrls(url, headers):
    rankingList = []
    req = requests.get(url=url, headers = headers)
    bs = BeautifulSoup(req.text, "html.parser")
    box = bs.select_one('div.ranking_inbox')
    lists = box.select('div.ranking_list')
    for l in lists:
        url = l.select_one('div.rank_h').select_one('a').attrs['href']
        rankingList.append(url)
    return rankingList

def scraping(urls, content):
    for url in urls:
        print(url)
        naros = Website(url, targetPattern, commentTag, bodyTag, errorTags)
        crawler = Crawler(naros, headers, content)
        crawler.crawl()



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"} #ユーザエージェント設定
targetPattern = '..\/impression\/list\/..'
commentTag = "div.waku > div.comment"
bodyTag = "#novel_honbun"
rankingUrl = "https://yomou.syosetu.com/rank/list/type/monthly_total/"
errorTags = ["#container", "#contents_main"]
urls = searchRankingUrls(rankingUrl, headers)
content = Content()
scraping(urls, content)
content.printing()
content.save("commet.txt", "body.txt")






