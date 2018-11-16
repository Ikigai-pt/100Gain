from sqlalchemy import Column, String, Date, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base, session_factory
import uuid

class VolatileStock(Base):
    __tablename__ = 'VolatileStock'
    uuid = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, primary_key=True)
    symbol = Column(String)
    price = Column(Numeric)
    change = Column(Numeric)
    category = Column(String)
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
            session.merge(existingStock)
        session.commit()
        session.close()

    def __init__(self, name=None, symbol=None, price=0.0, change=0.0, category=None, reportedDate=None):
        self.uuid = uuid.uuid4()
        self.name = name
        self.symbol = symbol
        self.price = price
        self.change = change
        self.category = category
        self.reportedDate = reportedDate

