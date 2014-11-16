#!/bin/env python
#coding:utf-8
from pyquery import PyQuery as pq

class Article:
  def __init__(self, url, category, title, content):
    self.url = url
    self.category = category
    self.title = title
    self.content = content

  def save_article(self):
    # DBに書き込むメソッド
    print 'save article to DB'

  def get_info(self):
    print self.category + ', ' + self.title
    print self.content
