import yfinance as yf
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def predict(ticker:str,period='5y'):
    df=yf.download(ticker, period='5y', auto_adjust=True)
    # 特徴量
    df['Return']=df['Close'].pct_change() # 前日からの変化率
    df['Volatility']=(df['High']-df['Low']).abs() # 価格の揺れ度
    df['Volume_change']=df['Volume'].pct_change() # 株の注目度
    df['Roll_5']=df['Close'].rolling(window=5).mean() # 短期のトレンド
    df['Roll_10']=df['Close'].rolling(window=10).mean() # 長期のトレンド
    df['MA_Ratio']=df['Roll_5']/df['Roll_10'] # 直近が上昇 or 下降傾向

    # 目的変数
    df['Label']=(df['Close'].shift(-1)>df['Close']).astype(int)

    # データ前処理
    df=df.droplevel('Ticker',axis=1)
    print(df.columns)
    print(df.tail(5))
    df=df.dropna(axis=0)
    x=df.loc[:,'Return':'MA_Ratio']
    t=df['Label']
    sc=StandardScaler()
    sc_x=sc.fit_transform(x)

    X_train,X_test,y_train,y_test=train_test_split(sc_x,t,test_size=0.1,random_state=0)

    # モデル学習 ランダムフォレスト
    model=RandomForestClassifier(n_estimators=200,random_state=0)
    model.fit(X_train,y_train)
    print('Random Forest Train score:',model.score(X_train,y_train))
    print('Random Forest Test score:',model.score(X_test,y_test))

    # 調整
    print(df['Label'].value_counts())
    importance=pd.Series(model.feature_importances_, index=x.columns)
    print(importance)

    # 訓練データの過学習（バリアンス）を防ぐため、正則化項を追加：　ロジスティック回帰
    model2=LogisticRegression(random_state=0,C=1)
    model2.fit(X_train,y_train)
    print('Logistic Regression Train score:',model2.score(X_train,y_train))
    print('Logistic Regression Test score:',model2.score(X_test,y_test))

    # モデル保存
    with open('model.pkl',mode='wb') as f:
        pickle.dump(model,f)
    with open('model2.pkl',mode='wb') as f:
        pickle.dump(model2,f)