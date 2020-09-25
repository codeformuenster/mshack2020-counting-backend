from sqlalchemy import Column, Integer, Float, DateTime, String, JSON
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
    device_id = Column(String, nullable=True)

    def __repr__(self):
        return f"Count({self.long}, {self.lat}: {self.count})"

# parameter for POST /counts
class CountParameter(BaseModel):
    long: float
    lat: float
    count: int
    timestamp: str
    device_id: str

# paramter model for `payload_fields` for POST /ttn_pax_counts
class TTNPayloadFields(BaseModel):
    longitude: float
    latitude: float
    wifi: int
    time: str

class TTNHTTPIntegrationParameter(BaseModel):
    payload_fields: TTNPayloadFields


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True)
    data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"Device({self.id}, {self.data})"

class DeviceModel(BaseModel):
    id: str
    data: dict
