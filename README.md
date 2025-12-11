# Name
あしたの株ラボ
--ティッカーと予測日数を入力すると、明日(or今日)の株価が上昇/下降するかの予測結果および結果の信頼度を返します。

# Architecture
フロントエンド：Next.js
バックエンド：FastAPI
　--機械学習：scikit-learn, pandas, yfinance
言語：python

# Requirement
Node.js v24.11.1で動作確認済み

# How to Setup
1. Gitクローンする
   git clone https://github.com/maaari330/stock-predictor-web/
2. バックエンドにインストール
   pip install sklearn pandas yfinance
3. フロントエンドにインストール
   cd stock-frontend
   pip install "fastapi[all]"  # fastAPI
   npm install react-icons --save　# React-icons
4. 実行
   npm run dev # フロント実行
   uvicorn main:app --reload　# fastAPI実行

# Demo

# Usage
http://localhost:3000 にアクセス
銘柄コード/Ticker と 日数 を入力し、株価予測ボタンをクリック

# License
'あしたの株ラボ' is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
yfinance(MIT Licence)は個人学習目的で使用しています。
   
