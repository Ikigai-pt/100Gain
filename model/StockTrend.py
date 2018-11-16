from sqlalchemy import Column, String, Date, Integer, Numeric, relationship
from db.base import Base, session_factory

class StockTrend(Base):
    __tablename__ = 'StockTrend'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    price = Column(Numeric)
    decision = Column(String)
    daysTracked = Column(Integer)
    lastTrackedDate = Column(Date)
    trends = relationship("DailyTrend")
    category = Column(String)
    reboundFrequency = Column(Numeric)

    def saveStockTrend(self):
        session = session_factory()
        existingStock = session.query(StockTrend).filter(StockTrend.symbol == self.symbol).first()
        if existingStock is None:
            session.add(self)
        else:
            existingStock.price = self.price
            existingStock.reportedDate = self.reportedDate
            existingStock.category = self.category
            session.merge(existingStock)
        session.commit()
        session.close()

    def __init__(self, name=None, symbol=None, price=0.0, change=0.0, category=None, decision=None):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.change = change
        self.category = category
        self.decision = decision

    def addDailyTrend(self, currentTrend):
        self.trend[self.daysTracked] = currentTrend
        if(currentTrend.reportedDate > self.lastTrackedDate ):
            self.lastTrackedDate = currentTrend.reportedDate
            self.daysTracked += 1




