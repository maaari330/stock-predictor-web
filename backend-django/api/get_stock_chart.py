import yfinance as yf

def get_stock_chart(ticker:str,metric:str,start:str,end:str):
    stock_df=yf.download(ticker,start=start,end=end)
    stock_df=stock_df.droplevel('Ticker',axis=1)

    # Volatility MA_Ratioを計算
    stock_df['Volatility']=(stock_df['High']-stock_df['Low']).abs()
    stock_df['Roll_5']=stock_df['Close'].rolling(window=5).mean() 
    stock_df['Roll_10']=stock_df['Close'].rolling(window=10).mean() 
    stock_df['MA_Ratio']=stock_df['Roll_5']/stock_df['Roll_10']

    metric_series={"dates":stock_df[metric].index.astype(str).tolist(),"values":stock_df[metric].tolist()}
    return metric_series