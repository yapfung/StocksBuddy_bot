# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:40:47 2021

@author: YF
"""

import yfinance as yf
import pandas_datareader as web
import mplfinance as fplt
# import plotly.figure_factory
# import plotly.io as pio
import datetime as dt
import re


def plot_candlesticks(text, stock_df):
    fplt.plot(stock_df, type='candle', style='charles', \
          ylabel='Price (USD)',volume=True, ylabel_lower='Volume',\
              title=text, show_nontrading=False, \
                  datetime_format = '%d-%B', \
                      savefig=dict(fname='stock.jpg', bbox_inches="tight"))

def get_stock_data(message):
    text = message.text.upper()
    text = re.sub(r'[^\w]', ' ', text)
    ticker = yf.Ticker(text)
    df = ticker.history(period='3mo')
    if df.empty:
        return None
    df = df.round(3)
    df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
    df['Date'] = df.index
    df['Date'] = df['Date'].dt.date
    reply = str(df.iloc[-1])
    reply = reply[:reply.rfind('\n')]
    plot_candlesticks(text,df)
    return reply


# def view_stock(message):
#     ticker = message.text.upper()
#     if ticker in web.get_nasdaq_symbols().index.to_list():
#         stock_df = web.get_data_stooq(ticker, \
#                             dt.datetime.now() - dt.timedelta(days=60))
#         stock_df = stock_df.iloc[::-1]
#         stock_df['Date'] = stock_df.index
#         stock_df['Date'] = stock_df['Date'].dt.date
#         reply = str(stock_df.iloc[-1])
#         reply = reply[:reply.rfind('\n')]
#         plot_candlesticks(ticker, stock_df)
#         return reply


        # fig = plotly.figure_factory.create_candlestick(stock_df.Open, \
            # stock_df.High, stock_df.Low, stock_df.Close, dates=stock_df.index)
        # fig.write_html('test.html')
        # # pio.write_image(fig, 'test.jpg')