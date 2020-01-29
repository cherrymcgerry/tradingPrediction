import pandas as pd
import matplotlib
import bs4 as bs
import pandas_datareader.data as web
import pickle
import requests
import os
import datetime as dt

def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'id' : 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    print(tickers)
    return tickers

def get_data_from_yahoo():

    if not os.path.isfile("sp500tickers.pickle"):
        print("getting tickers from wikipedia")
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs("stock_dfs")

    start = dt.datetime(2015,1,1)
    end = dt.datetime.now()

    for ticker in tickers:
        print(ticker)
        if not os.path.exists(F'stock_dfs/{ticker}.csv'):
            try:
                df = web.DataReader(ticker,'yahoo',start, end)
                df.to_csv(F'stock_dfs/{ticker}.csv')
            except Exception as ex:
                print('Error',ex)
        else:
            print(F'Already have {ticker}')


def get_stock_dataframes():

    if not os.path.exists('stock_dfs'):
        get_data_from_yahoo()

    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    dfs = []

    for count, ticker in enumerate(tickers):

        try:
            df = pd.read_csv(F"stock_dfs/{ticker}.csv")
            df.set_index('Date', inplace=True)
            dfs.append({'df': df, 'ticker': ticker})

        except Exception as ex:
            print('Error',ex)
    print(dfs)
    return dfs

get_stock_dataframes()



