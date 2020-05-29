import requests
from bs4 import BeautifulSoup
import urllib3
import certifi

def get_news():
    url = "https://news.yahoo.co.jp"
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')

    top_news=soup.select('[data-ual-gotocontent="true"]')

    news_top_list=[]
    news_top_url=[]
    for tag in top_news:
        if len(news_top_list)==8:
            break
        else:
            if tag.string is None:
                news_top_url.append(tag.attrs['href'])
                for tag2 in tag:
                    if tag2.string is None:
                        pass
                    else:
                        news_top_list.append(tag2.string)
            else:
                news_top_url.append(tag.attrs['href'])
                news_top_list.append(tag.string)
    return news_top_list, news_top_url
