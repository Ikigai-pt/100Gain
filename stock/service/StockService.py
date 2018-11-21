from bs4 import BeautifulSoup
from iexfinance import Stock
from datetime import date, timedelta
from model.StockTrend import StockTrend
from model.DailyTrend import DailyTrend
from db.base import session_factory
from decisionEngine.StockRule import applyRule
from decimal import Decimal
import math
def fetchStock(symbol):
    try:
        quote = Stock(symbol, output_format="json")
        stock = {}
        if quote is not None:
            stock['symbol'] = quote.get_quote()["symbol"]
            stock['name'] = quote.get_quote()["companyName"]
            stock['sector'] = quote.get_quote()["sector"]
            stock[ 'price' ] = quote.get_price()
            stock[ 'avgVolume' ] = quote.get_quote()["avgTotalVolume"]
            stock[ 'change' ] = quote.get_quote()["change"]
            stock[ 'changePercent' ] = quote.get_quote()["changePercent"]
            stock[ 'marketCap' ] = quote.get_quote()["marketCap"]
            stock[ 'week52High' ] = quote.get_quote()["week52High"]
            stock[ 'week52Low' ] = quote.get_quote()["week52Low"]
            stock[ 'reportedDate' ] = date.today()
            return stock
        else:
            print('symbol not found in Exchange')
            return None
    except Exception as err:
        print(err)
        return None

def dayTrendOfStock(stock):
    return None

def createNewStockTrend(stock):
    stock['daysTracked'] = 1
    stock['trackBeginDate'] = date.today()
    stock['changePercentSinceTracking'] = 0
    newStockTrend = StockTrend(stock)
    newStockTrend.addStock(stock)
    return newStockTrend

def updateExistingStock(stock, existingStock):
    stock['initPrice'] = existingStock.initPrice
    stock['category'] = existingStock.category
    stock['trackBeginDate'] = existingStock.trackBeginDate
    stock['changePercentSinceTracking'] = getDiffPercent(existingStock.initPrice, stock['price'])
    if(existingStock.lastTrackedDate < date.today() ):
        stock['daysTracked'] = existingStock.daysTracked + 1
    existingStock.addStock(stock)
    return existingStock

def upsertStockTrend(stock):
    # check if stock exists
    symbol = stock['symbol']
    existingStock = StockTrend.getStock(symbol)
    if existingStock is None:
        return createNewStockTrend(stock)
    else:
        return updateExistingStock(stock, existingStock)

def upsertDailyTrend(stockTrend):
    # insert new dayTrend
    dailyStock = DailyTrend(stockTrend.symbol, stockTrend.id, stockTrend.daysTracked, date.today())
    trend = {'status': 'None', 'changePercent': stockTrend.changePercent, 'price': stockTrend.price}
    result = dailyStock.addDayTrend(trend)
    return dailyStock.saveDayTrend()

def stockTrend(currentStock, category):
    symbol = currentStock['symbol']
    stock = {}
    stock['symbol'] = symbol
    stock['name'] = currentStock['name']
    stock['category'] = category
    stock['initPrice'] = currentStock['price']
    stock['price'] = currentStock['price']
    stock['change'] = currentStock['change']
    stock['changePercent'] = currentStock['changePercent']
    stock['trackEndDate'] = date.today()
    stock['lastTrackedDate'] = date.today()
    session = session_factory()
    updatedStock = upsertStockTrend(stock)
    session.add(updatedStock)
    session.flush()
    session.refresh(updatedStock)
    session.commit()
    print("Updated = stock %s %s "%(updatedStock.id, updatedStock.decision))
    upsertDailyTrend(updatedStock)
    decision = applyRule(DailyTrend.getTrends(symbol,updatedStock.id))
    session = session_factory()
    updatedStock.decision = decision
    print("Updated = stock %s %s "%(updatedStock.id, updatedStock.decision))
    session.merge(updatedStock)
    session.flush()
    session.commit()
    session.close()
    return updatedStock



def getDiffPercent(previous, current):
    if current == previous:
        return Decimal(0)
    try:
        result = Decimal(Decimal(current) - Decimal(previous))
        result = Decimal(result) / Decimal(previous)
        result = Decimal(result) * Decimal(100)
        return round(result,2)
    except ZeroDivisionError:
        return Decimal(0)

# def applyRule(symbol, stockId):
#     s = session_factory()
#     results = s.query(DailyTrend).filter_by(symbol=symbol, stockId= stockId).all()
#     dailyTrend = [r for r in results]
#     s.close()
#     rule = {"day1": "'N'", "day2": "'N'", "day3": "'N'", "Action": "'None'"}
#     for i in range(len(dailyTrend)):
#         stock = dailyTrend[i]
#         index = i + 1
#         if stock.changePercent > 0.0 :
#             rule["day"+str(stock.dayNumber)] = "'H'"
#         else:
#             rule["day"+str(stock.dayNumber)] = "'L'"
#     process_dt(rule, ruleBook)
#     print(rule)
#     return rule["Action"].replace('"', '')



# generateRuleData('AAPL', 1)


