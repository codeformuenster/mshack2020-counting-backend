from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    long = Column(Float)
    lat = Column(Float)
    count = Column(Float)

    def __repr__(self):
        return f"Count({self.long}, {self.lat}: {self.count})"
