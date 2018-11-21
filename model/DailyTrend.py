from datetime import date
from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base, session_factory

class DailyTrend(Base):
    __tablename__ = 'DailyTrend'
    id = Column(Integer, nullable=False, primary_key=True , autoincrement=True)
    status = Column(String)
    dayNumber = Column(Numeric)
    changePercent = Column(Numeric)
    symbol = Column(String)
    price = Column(Numeric)
    trackedDate = Column(Date)
    stockId = Column(Integer, ForeignKey('StockTrend.id'))

    def addDayTrend(self, stock):
        for key, value in stock.items():
            setattr(self, key, value)
        return self

    def getDayTrend(self, symbol, dateToFilter):
        s = session_factory()
        stock  = s.query(DailyTrend).filter(DailyTrend.symbol == symbol, DailyTrend.trackedDate == dateToFilter).first()
        s.close()
        if stock is None:
            return None
        else:
            return stock

    def saveDayTrend(self):
        session = session_factory()
        existingStock = self.getDayTrend(self.symbol, self.trackedDate)
        if existingStock is None:
            session.add(self)
        else:
            existingStock.price = self.price
            existingStock.stockId = self.stockId
            session.merge(existingStock)
        session.commit()
        session.close()
        return self

    @staticmethod
    def getTrends(symbol, stockId):
        s = session_factory()
        trends = s.query(DailyTrend).filter_by(symbol=symbol, stockId= stockId).all()
        s.close()
        return trends

    def __init__(self, symbol, stockId, dayNumber, reportedDate):
        self.symbol= symbol
        self.trackedDate = reportedDate
        self.stockId = stockId
        self.dayNumber = dayNumber

