from stock.service.StockService import fetchStock
from datetime import date
from App import app
from model.VolatileStock import VolatileStock

@app.task
def stockInfo(symbol, category):
    stock = fetchStock(symbol)
    if stock is not None:
        vStock = VolatileStock(
                category,
                date.today())
        vStock.addStock(stock)
        vStock.saveStock()

def get_change(current, previous):
    if current == previous:
        return 0.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0.0
