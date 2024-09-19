import yfinance as fy
# from app_utils import *
from app_utils import *
# from variables import *
import asyncio
import datetime
import pandas as pd
import json

async def get_ticker_price(ticker, type):
    info = yf.Ticker(ticker).info
    print(info)
    return float(info['currentPrice']) if type.lower() == "equity" else float(info['previousClose'])

# get_ticker_price()

def new_fun():
    ticker = "GPTINFRA.NS"
    start_date = "2024-08-28"
    end_date = "2024-08-29"
    # ticker = yf.Ticker(ticker)
    # data = yf.download(ticker, start=start_date, end=end_date)
    tic = yf.Ticker(ticker)
    data = tic.fast_info['lastPrice']
    print(data)

# new_fun()

def get_price_history(tickers_list, start_date, end_date):
    financial_data = {}
    for ticker in tickers_list:
        # ticker = yf.Ticker(ticker)
        data = yf.download(ticker, start=start_date, end=end_date)
        # print(data)
        parsed_data = json.dumps(data.to_json(date_format="iso"))
        # json.loads()
        share_price_data = json.loads(json.loads(parsed_data))['Close']
        # share_price_data = json.loads(json.loads(parsed_data))['currentPrice']
        # [] = []
# .day
        share_price = [[datetime.datetime.fromisoformat(x).strftime("%Y-%m-%d"), share_price_data[x]] 
                       for x in share_price_data.keys()]
        share_price = dict(share_price)

        # print(share_price_data)
        financial_data[ticker] = share_price

    # print("financial data", financial_data)
    return financial_data
    # printing share price map
    # [print(x, financial_data[x]) for x in financial_data.keys()]

