from stock.StockService import fetchStock
from stock.App import app
from model.VolatileStock import VolatileStock

@app.task
def stockInfo(symbol, category):
    stock = fetchStock(symbol)
    if stock is not None:
        vStock = VolatileStock(
                stock['symbol'],
                stock[ 'symbol' ],
                stock[ 'price' ],
                get_change(float(stock['price']), float(stock['previousPrice'])),
                category,
                stock[ 'updatedAt' ])
        vStock.saveStock()

def get_change(current, previous):
    if current == previous:
        return 0.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0.0
