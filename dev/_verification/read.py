#!/bin/env python
#coding:utf-8
import MeCab
import sys
import sqlite3
import gensim
import time
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation

import urllib2
from pyquery import PyQuery as pq



def get_words(dataArray):
  for i in dataArray:
    tagger = MeCab.Tagger (" ".join(sys.argv))
    node = tagger.parseToNode(i['title'] + i['content'])

    words = []
    while node:
      if node.feature.split(',')[0] == '名詞' :
        word = unicode(node.surface, 'utf-8', errors='ignore').encode('utf-8')
        words.append(word)
      node = node.next
    i['words'] = words

def key_list (ori_list, key):
  tmp_list = []
  for i in ori_list:
    tmp_list.append(i[key])
  return tmp_list

db = sqlite3.connect('train_data.db', isolation_level=None)
c = db.cursor()

sql = u"select * from train_data"
c.execute(sql)
train_data = []
for i in c:
  train_data.append({
    'category': i[0].encode('utf-8'),
    'title': i[1].encode('utf-8'),
    'content': i[2].encode('utf-8'),
    'url': i[3].encode('utf-8')
  });
db.close()

get_words(train_data)

print len(train_data), 'articles exists.'
all_words = []
for i in train_data:
  all_words.append(i['words'])

dictionary = gensim.corpora.Dictionary(all_words)
# dictionary.filter_extremes(no_below=100, no_above=0.3) #fastest
# dictionary.filter_extremes(no_below=1, no_above=0.6) #0.8905 0.9 88.9s best score
dictionary.filter_extremes(no_below=3, no_above=0.6)
# dictionary.filter_extremes(no_below=10, no_above=0.6)


print 'making dictionary has been completed.'

num = len(dictionary)
print 'making vec data.'
for i in train_data:
  i['bow'] = dictionary.doc2bow(i['words'])
  i['dense'] = list(gensim.matutils.corpus2dense([i['bow']], num_terms=num).T[0])


# 検証 #############################################################
timestart = time.clock()
x_train, x_test, y_train, y_test = cross_validation.train_test_split(key_list(train_data, 'dense'), key_list(train_data, 'category'), test_size=0.2, random_state=0)
estimator = GaussianNB()
estimator.fit(x_train, y_train)
score1 = estimator.score(x_test, y_test)
timeend = time.clock()
time1 = timeend - timestart
print 'GaussianNB: ', score1, round(time1, 3), 's'

# print 'GaussianNB: ', estimator.score(x_test, y_test)

# 実験 #####################################################
estimator.fit(key_list(train_data, 'dense'), key_list(train_data, 'category'))

def getAllData(url):
    d = pq(url)
    tmp = {
        'title': d('title').text().encode('utf-8'),
        'content': d('p').text().encode('utf-8'),
    }
    tagger = MeCab.Tagger (" ".join(sys.argv))
    node = tagger.parseToNode(tmp['title'] + tmp['content'])
    words = []
    while node:
      if node.feature.split(',')[0] == '名詞' :
        word = unicode(node.surface, 'utf-8', errors='ignore').encode('utf-8')
        words.append(word)
      node = node.next
    tmp['words'] = words
    tmp['bow'] = dictionary.doc2bow(tmp['words'])
    tmp['dense'] = list(gensim.matutils.corpus2dense([tmp['bow']], num_terms=num).T[0])
    return tmp

test = getAllData('http://www12.plala.or.jp/solaris_works/reports_001.html')
result = estimator.predict([test['dense']])
print result[0], '経済'

# estimator.fit(key_list(train_data, 'dense'), key_list(train_data, 'category'))
# print 'GaussianNB: ', estimator.score(x_test, y_test)




# 次元削減 #########################################################
# topics数の適切な設定を考えるべし 200 〜 500 が一般的？
# num_topics = 2
# num_topics = 300
num_topics = int(num * 0.30)
# lsi = gensim.models.LsiModel(key_list(train_data, 'bow'), id2word=dictionary, num_topics=num_topics)
lda = gensim.models.LdaModel(key_list(train_data, 'bow'), id2word=dictionary, num_topics=num_topics)
for i in train_data:
  # i['lsi'] = list(gensim.matutils.corpus2dense([lsi[i['bow']]], num_terms=num_topics).T[0])
  i['lda'] = list(gensim.matutils.corpus2dense([lda[i['bow']]], num_terms=num_topics).T[0])

# # 次元削減後の検証 ###################################################
timestart = time.clock()
# x_train, x_test, y_train, y_test = cross_validation.train_test_split(key_list(train_data, 'lsi'), key_list(train_data, 'category'), test_size=0.2, random_state=0)
x_train, x_test, y_train, y_test = cross_validation.train_test_split(key_list(train_data, 'lda'), key_list(train_data, 'category'), test_size=0.2, random_state=0)
estimator = GaussianNB()
estimator.fit(x_train, y_train)
score2 = estimator.score(x_test, y_test)
timeend = time.clock()
time2 = timeend - timestart
print 'GaussianNB+LSI: ', score2, round(time2, 3), 's'
print len(train_data[0]['dense']), '->', len(train_data[0]['lda'])
print '結果：精度は' + str(round((1 - score2 / score1) * 100, 2)) + '%低下したが、速度は' + str(round(time1 / time2 * 100 - 100, 2)) + '%高速化した。'
