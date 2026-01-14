### Name
あしたの株ラボ  
ティッカーと予測日数を入力すると、翌営業日の株価が上昇/下降するかの予測結果および結果の信頼度を返します。

### Architecture
-フロントエンド：Next.js  
-バックエンド：Django / Django REST Framework 
-機械学習：scikit-learn, pandas, yfinance  
-言語：python

### Requirement
-Python 3.10.11  
-Node.js v24.11.1で動作確認済み

### How to Setup
1. リポジトリのクローン  
   git clone https://github.com/maaari330/stock-predictor-web/  
   cd stock-predictor-web  
2. バックエンドのセットアップ  
   cd backend-django
   pip install -r requirements.txt
   python manage.py migrate
3. フロントエンドのセットアップ  
   cd stock-frontend  
   npm install  
   npm install react-icons --save　# React-icons  
4. 起動  
   cd backend-django
   python manage.py runserver　# バックエンド（Django） 
   cd stock-frontend 
   npm run dev # フロント（別ターミナル）  

### Demo

### Usage
http://localhost:3000 にアクセス  
銘柄コード/Ticker と 日数 を入力し、株価予測ボタンをクリック  

### License
'あしたの株ラボ' is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).  
yfinance(MIT Licence)は個人学習目的で使用しています。
   
