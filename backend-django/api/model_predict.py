import yfinance as yf
import pandas as pd
import pickle
from pathlib import Path

def model_predict(ticker:str,symbol:str,period='60d'):
    # データ取得
    stock_df=yf.download(ticker, period=period, auto_adjust=True)
    fx_df = yf.download(symbol, period=period, interval="1d")
    fx_df=fx_df.rename(columns=lambda s: 'Fx_'+s)
    df=pd.merge(stock_df,fx_df,left_index=True,right_index=True)
    df=df.droplevel('Ticker',axis=1)

    # 特徴量（株価）
    df['Return']=df['Close'].pct_change() # 前日からの変化率
    df['Volatility']=(df['High']-df['Low']).abs() # 価格の揺れ度
    df['Volume_change']=df['Volume'].pct_change() # 株の注目度
    df['Roll_5']=df['Close'].rolling(window=5).mean() # 短期のトレンド
    df['Roll_10']=df['Close'].rolling(window=10).mean() # 長期のトレンド
    df['MA_Ratio']=df['Roll_5']/df['Roll_10'] # 直近が上昇 or 下降傾向

    # 特徴量（為替）
    df['Fx_Return']=df['Fx_Close'].pct_change() # 前日からの変化率
    df['Fx_Volatility']=(df['Fx_High']-df['Fx_Low']).abs() # 為替の揺れ度
    df['Fx_Roll_5']=df['Fx_Close'].rolling(window=5).mean() # 短期のトレンド
    df['Fx_Roll_10']=df['Fx_Close'].rolling(window=10).mean() # 長期のトレンド
    df['Fx_MA_Ratio']=df['Fx_Roll_5']/df['Fx_Roll_10'] # 直近の為替が上昇 or 下降傾向 = 短期のトレンド / 長期のトレンド
    df['Fx_Return_lag1d']=df['Fx_Return'].shift(periods=1)  # 前々日 → 前日 間の為替変化率

    # モデル、特徴量の列名、しきい値をロード
    BASE_DIR = Path(__file__).resolve().parent
    model = pickle.load(open(BASE_DIR / "model_randomforest.pkl", "rb"))
    feature_cols = pickle.load(open(BASE_DIR / "feature_cols.pkl", "rb"))
    threshold = float(pickle.load(open(BASE_DIR / "threshold.pkl", "rb")))

    # データ前処理
    df=df.dropna(axis=0)
    # データが足りない場合（period短すぎ等）
    if len(df) == 0:
        return {"error": "Not enough data to compute features. Try longer period (e.g., 90d)."}
    x=df.loc[:,feature_cols].tail(1)
    
    # 株価が上がる確率、下がる確率を出す
    probability = model.predict_proba(x)[0]
    down_probability = float(probability[0])
    up_probability = float(probability[1])
    direction = "上昇予想" if up_probability >= threshold else "下落予想"
    margin = abs(up_probability - threshold)
    strength = margin * 100 / max(threshold, 1 - threshold)

    # 戻り値
    return {
        'UpPercent': round(up_probability * 100, 1),
        'DownPercent': round(down_probability * 100, 1),
        'Direction': direction,
        'Strength':strength,
    }
