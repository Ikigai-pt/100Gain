from datetime import date
class StockTrend:
    trend = {}
    daysTracked = 0
    lastTrackedDate= date.today()

    def __init__(self, symbol, name, price):
        self.name = name
        self.symbol = symbol
        self.price = price

    def addDailyTrend(self, currentTrend):
        self.trend[self.daysTracked] = currentTrend
        if(currentTrend.reportedDate > self.lastTrackedDate ):
            self.lastTrackedDate = currentTrend.reportedDate
            self.daysTracked += 1




