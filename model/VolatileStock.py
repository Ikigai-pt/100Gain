from sqlalchemy import Column, String, Date, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base, session_factory
import uuid

class VolatileStock(Base):
    __tablename__ = 'VolatileStock'
    uuid = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, primary_key=True)
    category = Column(String)
    symbol = Column(String)
    price = Column(Numeric)
    avgVolume = Column(Numeric)
    change = Column(Numeric)
    changePercent = Column(Numeric)
    marketCap = Column(Numeric)
    week52High = Column(Numeric)
    week52Low = Column(Numeric)
    reportedDate = Column(Date)

    def saveStock(self):
        session = session_factory()
        existingStock = session.query(VolatileStock).filter(VolatileStock.symbol == self.symbol).first()
        if existingStock is None:
            session.add(self)
        else:
            existingStock.price = self.price
            existingStock.reportedDate = self.reportedDate
            existingStock.category = self.category
            existingStock.change = self.change
            existingStock.changePercent = self.changePercent
            session.merge(existingStock)
        session.commit()
        session.close()

    def addStock(self, stock):
        for key, value in stock.items():
            print(value)
            setattr(self, key, value)

    def __init__(self, category, reportedDate):
        self.uuid = uuid.uuid4()
        self.category = category
        self.reportedDate = reportedDate

