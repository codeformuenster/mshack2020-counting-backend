from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel


Base = declarative_base()


class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    long = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Count({self.long}, {self.lat}: {self.count})"

class CountParameter(BaseModel):
    long: float
    lat: float
    count: int
    timestamp: str
