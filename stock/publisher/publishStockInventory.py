from stock.tasks.managerStock import classifier
from model.StockTrend import StockTrend
# load stocks from StockTrend days > 4
def classifyStocks():
    stocks = StockTrend.getStocks()
    for stock in stocks:
        classifier.delay(stock.symbol)
if __name__ == '__main__':
    print("Classify Stocks")
    classifyStocks()
    # print("Top Losers")
    #
