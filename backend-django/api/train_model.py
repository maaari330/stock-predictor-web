import yfinance as yf
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from .models import TrainedModel

def train_model(ticker='7203.T',fx='USDJPY=X',period='10y'):
    # データ取得・結合
    stock_df=yf.download(ticker, period=period, auto_adjust=True)
    fx_df=yf.download(fx,period=period,interval='1d')
    fx_df=fx_df.rename(columns=lambda s: 'Fx_'+s)
    df=pd.merge(stock_df,fx_df,left_index=True,right_index=True)
    df=df.droplevel('Ticker',axis=1)

    print("df start:", df.index.min())
    print("df end:", df.index.max())
    print("df length:", len(df))


    # 特徴量（株価）
    df['Return']=df['Close'].pct_change() # 前日からの変化率
    df['Volatility']=(df['High']-df['Low']).abs() # 価格の揺れ度
    df['Volume_change']=df['Volume'].pct_change() # 株の注目度
    df['Roll_5']=df['Close'].rolling(window=5).mean() # 短期のトレンド
    df['Roll_10']=df['Close'].rolling(window=10).mean() # 長期のトレンド
    df['MA_Ratio']=df['Roll_5']/df['Roll_10'] # 直近の株価が上昇 or 下降傾向 = 短期のトレンド / 長期のトレンド

    # 特徴量（為替）
    df['Fx_Return']=df['Fx_Close'].pct_change() # 前日からの変化率
    df['Fx_Volatility']=(df['Fx_High']-df['Fx_Low']).abs() # 為替の揺れ度
    df['Fx_Roll_5']=df['Fx_Close'].rolling(window=5).mean() # 短期のトレンド
    df['Fx_Roll_10']=df['Fx_Close'].rolling(window=10).mean() # 長期のトレンド
    df['Fx_MA_Ratio']=df['Fx_Roll_5']/df['Fx_Roll_10'] # 直近の為替が上昇 or 下降傾向 = 短期のトレンド / 長期のトレンド
    df['Fx_Return_lag1d']=df['Fx_Return'].shift(periods=1)  # 前々日 → 前日 間の為替変化率

    # 目的変数（翌営業日の株価が上昇/下落するかの予測結果）
    df['Label']=(df['Close'].shift(-1)>df['Close']).astype(int)

    # データ前処理
    df = df.replace([np.inf, -np.inf], np.nan)
    df=df.dropna(axis=0)
    x=df.loc[:,'Return':'Fx_Return_lag1d']
    t=df['Label']
    scaler=StandardScaler()
    x_scaled = scaler.fit_transform(x)
    print(df['Label'].value_counts()) # 正解データ内の0,1の個数偏りなし

    # 混同行列用の正解データ・予測結果を保存するリスト
    all_true=[]
    all_predict_proba=[]

    # しきい値
    thresholds=[0.5,0.55,0.6,0.65,0.7]
    all_threshold_results = []

    # ロジスティック回帰モデル
    lr=LogisticRegression(solver="liblinear", max_iter=2000, random_state=0)

    # 学習・テストデータの分割
    tscv=TimeSeriesSplit(n_splits=5)

    for train_index,test_index in tscv.split(x,t):
        X_train=x_scaled[train_index]
        X_test=x_scaled[test_index]
        y_train=t.iloc[train_index]
        y_test=t.iloc[test_index]

        # 学習
        lr.fit(X_train, y_train)

        # 混同行列、点数計算のために正解データ・予測結果を保存
        lr_predict_proba=lr.predict_proba(X_test)[:,1]
        all_true.append(y_test)
        all_predict_proba.append(lr_predict_proba)
    
    # 混同行列の合算
    lr_y_true=pd.concat(all_true)
    lr_y_pred=np.concatenate(all_predict_proba)
        
    # しきい値ごとのFPとprecision(1)、accuracyを計算
    for threshold in thresholds:
        lr_y_result=(lr_y_pred>=threshold).astype(int)
        true_negative,false_positive,false_negative,true_positive=confusion_matrix(lr_y_true,lr_y_result).ravel()
        precision_1 = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall_0 = true_negative / (true_negative + false_positive) if (true_negative + false_positive) > 0 else 0
        recall_1 = true_positive / (true_positive + false_negative) if (true_positive + false_negative)>0 else 0.0
        f1_1 = (2 * precision_1 * recall_1 / (precision_1 + recall_1)) if (precision_1 + recall_1)>0 else 0.0
        accuracy = (lr_y_result == lr_y_true).mean()
        all_threshold_results.append({"threshold":threshold,"accuracy":accuracy,"recall_0":recall_0,"false_positive":false_positive, "precision_1":precision_1,"recall_1":recall_1,"f1_1":f1_1 })
    
    df_threshold = pd.DataFrame(all_threshold_results, columns=["threshold", "accuracy","recall_0","false_positive", "precision_1", "recall_1", "f1_1"])
    df_safe = df_threshold[df_threshold["recall_0"] >= 0.95]
    best_row =df_safe.sort_values("accuracy", ascending=False).iloc[0] # recall_0が95%以上で、その中でaccuracyが最大
    best_threshold=best_row["threshold"]
    print(df_threshold)
    print("best_threshold:", best_threshold)

    model=lr.fit(x_scaled,t)

    # モデルをDBへ保存
    model_bytes = pickle.dumps(model)
    threshold_value = float(best_threshold)
    feature_cols_list = list(x.columns)
    object = TrainedModel(ticker=ticker,fx=fx, model_data=model_bytes, threshold=threshold_value,feature_cols=feature_cols_list,)
    object.save()

    # （参考情報）重要な特徴量の洗い出し
    # importance=pd.Series(model.feature_importances_, index=x.columns).abs().sort_values(ascending=False)
    # print(importance)

    final_pred = (lr_y_pred >= best_threshold).astype(int) # 0,1に変換
    print("final accuracy:", (final_pred == lr_y_true).mean())
    print(classification_report(lr_y_true, final_pred))

if __name__ == '__main__':
    # 混同行列の確認
    train_model(ticker='7203.T',fx='USDJPY=X',period='20y')