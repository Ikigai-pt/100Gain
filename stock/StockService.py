from bs4 import BeautifulSoup
import requests
import pandas_datareader.data as web

def fetchStock(symbol):
    try:
        stock = {'symbol':None, 'price':0.0, 'previousPrice':0.0, 'updatedAt':None }
        df = web.get_quotes_robinhood(symbol)
        if df is not None:
            stock['symbol'] = symbol
            stock[ 'price' ] = df[symbol]['last_trade_price']
            stock[ 'previousPrice' ] = df[symbol]['previous_close']
            stock[ 'updatedAt' ] = df[symbol]['updated_at']
            return stock
        else:
            print('symbol not found in Exchange')
            return None
    except Exception as err:
        print(err)
        return None

