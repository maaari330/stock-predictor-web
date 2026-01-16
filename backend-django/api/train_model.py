import yfinance as yf
import pandas as pd
import pickle
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def train_model(ticker:str,fx_num:str,period='5y'):
    # データ取得・結合
    stock_df=yf.download(ticker, period=period, auto_adjust=True)
    fx_df=yf.download(fx_num,period=period,interval='1d')
    df=pd.merge(stock_df,fx_df,left_index=True,right_index=True)

    print(df.columns)

    # 特徴量
    df['Return']=df['Close'].pct_change() # 前日からの変化率
    df['Volatility']=(df['High']-df['Low']).abs() # 価格の揺れ度
    df['Volume_change']=df['Volume'].pct_change() # 株の注目度
    df['Roll_5']=df['Close'].rolling(window=5).mean() # 短期のトレンド
    df['Roll_10']=df['Close'].rolling(window=10).mean() # 長期のトレンド
    df['MA_Ratio']=df['Roll_5']/df['Roll_10'] # 直近が上昇 or 下降傾向 = 短期のトレンド / 長期のトレンド

    # 目的変数
    df['Label']=(df['Close'].shift(-1)>df['Close']).astype(int)

    # データ前処理
    df=df.droplevel('Ticker',axis=1)
    print(df.columns)
    print(df.tail(5))
    df=df.dropna(axis=0)
    x=df.loc[:,'Return':'MA_Ratio']
    t=df['Label']

    print(df['Label'].value_counts()) # 関会データ内の0,1の個数偏りなし

    best = {
        "score": -1.0,
        "model_name": None,
        "model": None,
        "scaler": None,
    }

    # 学習・テストデータの分割
    # X_train,X_test,y_train,y_test=train_test_split(sc_x,t,test_size=0.1,random_state=0)
    tscv=TimeSeriesSplit(n_splits=5)
    for train_index,test_index in tscv.split(x,t):
        X_train=x.iloc[train_index]
        X_test=x.iloc[test_index]
        y_train=t.iloc[train_index]
        y_test=t.iloc[test_index]
        sc=StandardScaler()
        sc_X_train=sc.fit_transform(X_train)
        sc_X_test=sc.transform(X_test)

        # モデル学習 ランダムフォレスト
        rf = RandomForestClassifier(n_estimators=200, random_state=0)
        rf.fit(sc_X_train, y_train)
        rf_test_score = rf.score(sc_X_test, y_test)

        if rf_test_score > best["score"]:
            best["score"] = rf_test_score
            best["model_name"] = "RandomForest"
            best["model"] = rf
            best["scaler"] = sc

        # 調整
        print(df['Label'].value_counts())
        importance=pd.Series(rf.feature_importances_, index=x.columns)
        print(importance)

        # 訓練データの過学習（バリアンス）を防ぐため、正則化項を追加：　ロジスティック回帰
        lr = LogisticRegression(random_state=0, C=1, max_iter=1000)
        lr.fit(sc_X_train, y_train)
        lr_test_score = lr.score(sc_X_test, y_test)

        if lr_test_score > best["score"]:
            best["score"] = lr_test_score
            best["model_name"] = "LogisticRegression"
            best["model"] = lr
            best["scaler"] = sc
    
    print("BEST:", best["model_name"], best["score"])

    # モデル保存
    with open('scaler.pkl',mode='wb') as f:
        pickle.dump(best["scaler"],f)
    with open('model.pkl',mode='wb') as f:
        pickle.dump(best["model"],f)

if __name__=='__main__':
    ticker='NVDA'
    fx_num='USDJPY=X'
    train_model(ticker,fx_num)