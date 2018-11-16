from datetime import date
from sqlalchemy import Column, String, Date, Integer, Numeric, relationship, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base, session_factory

class DailyTrend(Base):
    __tablename__ = 'DailyTrend'
    id = Column(Integer, nullable=False, primay_key=True )
    parent_id = Column(Integer, ForeignKey('StockTrend.id'))
    name = Column(String)
    action = Column(String)
    percentageChange = Column(Numeric)
    percentageChangeSinceTracking = Column(Numeric)
    symbol = Column(String)
    price = Column(Numeric)
    trackedDate = Column(Date)

    def __init__(self, price, action, pChangeSinceTracking, pChange, category):
        self.price = price
        self.action = action
        self.percentageChangeSinceTracking = pChangeSinceTracking
        self.percentageChange = pChange
        self.category = category
        self.action = action

