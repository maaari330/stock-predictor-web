import yfinance as yf
import pandas as pd
import pickle
from pathlib import Path

def model_predict(ticker:str,period='60d'):
    # データ取得
    df=yf.download(ticker, period=period, auto_adjust=True)

    # 特徴量
    df['Return']=df['Close'].pct_change() # 前日からの変化率
    df['Volatility']=(df['High']-df['Low']).abs() # 価格の揺れ度
    df['Volume_change']=df['Volume'].pct_change() # 株の注目度
    df['Roll_5']=df['Close'].rolling(window=5).mean() # 短期のトレンド
    df['Roll_10']=df['Close'].rolling(window=10).mean() # 長期のトレンド
    df['MA_Ratio']=df['Roll_5']/df['Roll_10'] # 直近が上昇 or 下降傾向

    # データ前処理
    df=df.droplevel('Ticker',axis=1)
    print(df.columns)
    print(df.tail(5))
    df=df.dropna(axis=0)
    x=df.loc[:,'Return':'MA_Ratio'].tail(1)
    print(x)
    BASE_DIR = Path(__file__).resolve().parent
    scaler_path = BASE_DIR / "scaler.pkl"
    sc=pickle.load(open(scaler_path,mode='rb'))
    sc_x=sc.transform(x)

    # モデルをロード
    model_path = BASE_DIR / "model2.pkl"
    model2=pickle.load(open(model_path,mode='rb'))
    Prediction=int(model2.predict(sc_x)[0])
    PredictionLabel='UP' if Prediction==1 else 'Down'
    Confidence=float(max(model2.predict_proba(sc_x)[0]))

    # 戻り値
    return {'Prediction':Prediction,'PredictionLabel':PredictionLabel,'Confidence':Confidence}
