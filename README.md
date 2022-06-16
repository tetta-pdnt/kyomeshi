# 今日飯 -KYOMESHI-
https://kyomeshi.herokuapp.com/

# 概要
複数人で食べに行くのに最適な料理を提案するwebアプリ
それぞれの空腹度や食嗜好を簡単なアンケート形式の回答から考慮し、近くの飲食店を提案します

# 使用技術・サービス
- Python
  - flask（バックエンドで使用）
- JavaScript
  - mapbox（地図表示に使用）
- heroku（実行環境）
- ホットペッパーグルメAPI
<a href="http://webservice.recruit.co.jp/"><img src="http://webservice.recruit.co.jp/banner/hotpepper-s.gif" alt="ホットペッパー Webサービス" width="135" height="17" border="0" title="ホットペッパー Webサービス"></a>

# きっかけ
ハッカソンイベント
イベント終了時は料理提案まで実装していました。その後、個人的にホットペッパーグルメAPIを利用して現在地周辺の飲食店を提案するところまで実装しました

# アピールポイント
提案の根拠となる各料理の嗜好データ(component.csv)は50人に対する事前調査により決定しています。また回答データとの距離的上位を単に提案するのではなく、距離をもとにした確率分布によって決定しているので、全く同じ回答をしてもバラエティに富んだ料理を提案することができます
