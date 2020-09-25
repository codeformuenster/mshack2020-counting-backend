from typing import Optional
from sqlalchemy import Column, Integer, Float, DateTime, String, JSON
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel


Base = declarative_base()


# Database models


class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    device_id = Column(String, nullable=False)
    data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"Count({self.id}, {self.timestamp}: {self.count})"


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"Device({self.id}, {self.lon}, {self.lat}, {self.data})"


# Parameters

# parameter for POST /counts
class CountParameter(BaseModel):
    device_id: str
    count: int
    timestamp: str
    data: Optional[dict] = None


# paramter model for `payload_fields` for POST /ttn_pax_counts
class TTNPayloadFields(BaseModel):
    longitude: float
    latitude: float
    wifi: int


class TTNMetadata(BaseModel):
    time: str


class TTNHTTPIntegrationParameter(BaseModel):
    dev_id: str
    payload_fields: TTNPayloadFields
    metadata: TTNMetadata


class DeviceParameter(BaseModel):
    id: str
    lat: float
    lon: float
    data: Optional[dict] = None
