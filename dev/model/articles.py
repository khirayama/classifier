#!/bin/env python
#coding:utf-8
from pyquery import PyQuery as pq
from article import Article

class Articles:
  def __init__(self):
    self.collection = []

  def set_yahoo_articles(self):
    page = 3
    url_list_yahoo = [
      {'category': '国内', 'url': ['http://news.yahoo.co.jp/list/?c=domestic']},
      {'category': '国際', 'url': ['http://news.yahoo.co.jp/list/?c=world']},
      {'category': '経済', 'url': ['http://news.yahoo.co.jp/list/?c=economy']},
      {'category': 'エンタメ', 'url': ['http://news.yahoo.co.jp/list/?c=entertainment']},
      {'category': 'スポーツ', 'url': ['http://news.yahoo.co.jp/list/?c=sports']},
      {'category': 'IT', 'url': ['http://news.yahoo.co.jp/list/?c=computer']},
      {'category': '科学', 'url': ['http://news.yahoo.co.jp/list/?c=science']},
      {'category': '地域', 'url': ['http://news.yahoo.co.jp/list/?c=local']}
    ]
    # make url list
    for item in url_list_yahoo:
      for page_num in range(2, page):
        url = item['url'][0] + '&p=' + str(page_num)
        item['url'].append(url)

    # make Article
    for item in url_list_yahoo:
      for page_num in range(0, page - 1):
        d = pq(item['url'][page_num])

        for (title, url) in zip(d('.list .ttl'), d('.list a')):
          url = 'http://news.yahoo.co.jp' + d(url).attr('href')
          category = item['category']
          title = d(title).text().encode('utf-8')
          content = pq(url)('.hbody').text().encode('utf-8')

          article = Article(url, category, title, content)
          article.get_info()
          self.collection.append(article)

collection = Articles()
collection.set_yahoo_articles()

