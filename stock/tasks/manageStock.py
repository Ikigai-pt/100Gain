import json
import requests
import pandas_datareader.data as web
from model.StockTrend import StockTrend
from stock.service.StockService import fetchStock, stockTrend
from App import app
from model.VolatileStock import VolatileStock
from datetime import date
from bs4 import BeautifulSoup
from celery import chain
losers_url= "https://finance.yahoo.com/losers?offset=0&count=100"
from config.celeryconfig import MARKET_CLOSED_DATES

@app.task
def stockInfo(symbol, category):
    if not isMarketOpen():
        print('MARKET IS CLOSED')
        return None
    stock = fetchStock(symbol)
    if stock is not None:
        vStock = VolatileStock(category, date.today())
        vStock.addStock(stock)
        vStock.saveStock()
        return stock
    return None

@app.task
def registerStock(symbol, category):
    if not isMarketOpen():
        print('MARKET IS CLOSED')
        return None
    stock = fetchStock(symbol)
    if stock is not None:
        stockTrend(stock, category)
    return "registered"

@app.task
def classifier(symbol, category):
    if not isMarketOpen():
        print('MARKET IS CLOSED')
        return None
    stock = fetchStock(symbol)
    if stock is not None:
        stockTrend(stock, category)
    return "classified"

@app.task
def publishVolatileStock():
    print("STARTED PUBLISHER")
    if not isMarketOpen():
        print('MARKET IS CLOSED')
        return None
    gainers = gatherStocks('gainers')
    losers = gatherStocks('losers')
    combinedStocks = gainers + losers
    for stock in combinedStocks:
        symbol = stock['symbol']
        category = stock['category']
        result = stockInfo.delay(symbol, category)
        registered = registerStock.delay(symbol, category)
        print("Finished %s" %(stock['symbol']))

@app.task
def classifyStocks():
    stocks = StockTrend.getStocks()
    for stock in stocks:
        classifier.delay(stock.symbol)

def gatherStocks(category):
    base_url = "https://finance.yahoo.com/"+category+"?offset=0&count=100"
    r  = requests.get(base_url)
    data = r.text
    result = BeautifulSoup(data,"html.parser")
    stocks = []
    for row in result.find_all('td'):
        link = row.a
        if link is not None :
            symbol = link['href'].split('=')[1]
            stock = { 'symbol': symbol, 'category': category }
            stocks.append(stock)
    return stocks

def isMarketOpen():
    print(MARKET_CLOSED_DATES)
    print(date.today())
    if date.today().strftime('%Y-%m-%d') in MARKET_CLOSED_DATES :
        return False
    else:
        return True

