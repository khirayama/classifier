#!/bin/env python
#coding:utf-8
import urllib2
import sqlite3
from pyquery import PyQuery as pq

db = sqlite3.connect('train_data.db', isolation_level=None)
c = db.cursor()
sql = u"create table train_data (category text, title text, content text, url text UNIQUE);"
try:
  c.execute(sql)
except:
  print "already exist."


def get_data(data_array, cat, url, domain, title_dom, anchor_dom):
  d = pq(url)
  for (title, anchor) in zip(d(title_dom), d(anchor_dom)):
    data_array.append({
      'category': cat,
      'title': d(title).text().encode('utf-8'),
      'content': '',
      'url': domain + d(anchor).attr('href')
    })
  print url, 'has been completed.'


print 'start to get articles...'
page = 5
data_sample = []

# make url list
url_list_yahoo = [
  {'category': '国内', 'url': ['http://news.yahoo.co.jp/list/?c=domestic']},
  {'category': '国際', 'url': ['http://news.yahoo.co.jp/list/?c=world']},
  {'category': '経済', 'url': ['http://news.yahoo.co.jp/list/?c=economy']},
  {'category': 'エンタメ', 'url': ['http://news.yahoo.co.jp/list/?c=entertainment']},
  {'category': 'スポーツ', 'url': ['http://news.yahoo.co.jp/list/?c=sports']},
  {'category': 'テクノロジー', 'url': ['http://news.yahoo.co.jp/list/?c=computer']}
]
for category in url_list_yahoo:
  for page_num in range(2, page + 1):
    url = category['url'][0] + '&p=' + str(page_num)
    category['url'].append(url)

# get data
for category in url_list_yahoo:
  for url in category['url']:
    get_data(data_sample, category['category'], url, 'http://news.yahoo.co.jp', '.list .ttl', '.list a')

# create traindata
print "create traindata...."
for i in data_sample:
  try:
    c.execute(u"insert into train_data values (?, ?, ?, ?)", (unicode(i['category'], 'utf-8'), unicode(i['title'], 'utf-8'), unicode(i['content'], 'utf-8'), unicode(i['url'], 'utf-8')))
  except:
    print "already exist.",

# read traindata
print "\nread traindata..."
train_data = []
sql = u"select * from train_data"
c.execute(sql)
for i in c:
  train_data.append({
    'category': i[0].encode('utf-8'),
    'title': i[1].encode('utf-8'),
    'content': i[2].encode('utf-8'),
    'url': i[3].encode('utf-8')
  })

# upadate traindata
print "\nupdate traindata..."
for i in train_data:
  if i['content'] == '':
    co = pq(i['url'])
    if i['url'].find('yahoo') > -1:
      content = co('.hbody').text().encode('utf-8')

    if(len(content)):
      print 'update content:', i['url']
      i['content'] = content
      c.execute(u"update train_data set content = ? where url = ?;", (unicode(i['content'], 'utf-8'), i['url']))
    else:
      print 'delete record:', i['url']
      c.execute(u"delete from train_data where url = ?;", (i['url'],))

db.close()

