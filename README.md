クラスタリング
=================

urlを投げると、その記事のカテゴリを返してくれる。  
SmartNewsやGunosyのようなキュレーションと同様のアルゴリズム。  

# とりあえずやってみたいとき。
ダウンロードして、read.pyを実行したらいけます。  
l107,108が予測したいurlとその正解カテゴリ（なくてもよいです。）  
l118から次元削減やってみてますが、データ数があまり多くないのと、
学習結果保存させてないので恩恵少ないです。

/dev/_verificationget
- できるか不明だったので、検証のための殴り書きコード
- get_sample_data.py: 学習用データ収集のスクレイピングコード
- read.py: 学習及び予測のコード。（学習結果を保存はしてない。命名がやばいw）
- train_data.db: ちょっと収集してみたデータなので、気になった人は、これでどんなもんか見てみてね。

/dev/model
- _じゃないディレクトリにちゃんと整理中....（手が回ってない（白目
- Django使ってウェブアプリ & API提供までやってみる。

参考  
http://stmind.hatenablog.com/entry/2013/11/04/164608  
http://yuku-tech.hatenablog.com/entry/20110623/1308810518  
http://developer.smartnews.com/blog/2013/08/19/lda-based-channel-categorization-in-smartnews/  
http://developer.smartnews.com/blog/2013/07/23/bayes-classification-based-channel-categorization-in-smartnews/  
