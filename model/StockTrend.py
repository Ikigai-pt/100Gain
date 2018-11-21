from sqlalchemy import Column, String, Date, Integer, Numeric, UniqueConstraint
from db.base import Base, session_factory
from sqlalchemy.orm import relationship, backref

class StockTrend(Base):
    __tablename__ = 'StockTrend'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    trackBeginDate = Column(Date, nullable=False)
    name = Column(String)
    symbol = Column(String)
    initPrice = Column(Numeric)
    price = Column(Numeric)
    change = Column(Numeric)
    changePercent = Column(Numeric)
    changePercentSinceTracking = Column(Numeric)
    decision = Column(String)
    daysTracked = Column(Integer)
    trackEndDate = Column(Date)
    lastTrackedDate = Column(Date)
    category = Column(String)
    reboundFrequency = Column(Numeric)
    trend = relationship('DailyTrend', primaryjoin="StockTrend.id == DailyTrend.stockId")

    def addStock(self, stock):
        for key, value in stock.items():
            setattr(self, key, value)
        return self

    @staticmethod
    def getStock(symbol):
        s = session_factory()
        stock  = s.query(StockTrend).filter(StockTrend.symbol == symbol, StockTrend.daysTracked <= 4).first()
        s.close()
        if stock is None:
            return None
        else:
            return stock

    @staticmethod
    def saveStockTrend(stock):
        session = session_factory()
        session.add(stock)
        print(stock)
        session.commit()
        session.close()

    @staticmethod
    def getStocks():
        s = session_factory()
        stocks = s.query(StockTrend).filter(StockTrend.daysTracked <= 4).all()
        s.close()
        return stocks

    def __init__(self, symbol):
        self.symbol = symbol

    def addDailyTrend(self, currentTrend):
        self.trend[self.daysTracked] = currentTrend
        if(currentTrend.reportedDate > self.lastTrackedDate ):
            self.lastTrackedDate = currentTrend.reportedDate
            self.daysTracked += 1




