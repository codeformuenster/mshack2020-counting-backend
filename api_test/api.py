from fastapi import FastAPI
from sqlsoup import SQLSoup

from api_test import db, model

app = FastAPI()

engine = db.get_db_engine()
db = SQLSoup(engine)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/counts")
def read_count_ids():
    """ Get all count ids """
    ids = [count.id for count in db.counts.all()]
    return {"count_ids": ids}


@app.get("/counts/{count_id}")
def read_count(count_id: int) -> model.Count:
    """ Read count for a given ID.

    Args:

        count_id (int): ID of count to be read

    Returns:

        Count: Count entry
    """
    count = db.counts.filter(db.counts.id == count_id).one()
    return {"count": count}


@app.post("/counts/", status_code=201)
async def create_count(count: model.CountParameter):
    """ Insert new count into database.

    Args:

        long (float): Longitude of count

        lat (float): Latitude of count

        count (int): Count value

        timestamp (str): Timestamp in ISO8601 notation

        device_id (str): device id from devices endpoint
    """
    inserted_count = db.counts.insert(long=count.long, lat=count.lat, count=count.count, timestamp=count.timestamp, device_id=count.device_id)
    db.commit()
    return {
        "inserted": True,
        "count_id": inserted_count.id
    }


@app.post("/ttn_pax_counts/", status_code=201)
async def create_count(count: model.TTNHTTPIntegrationParameter):
    """ Endpoint for TTN HTTP integration sending pax counter data.
    """
    data = count.dict()
    payload = data['payload_fields']
    inserted_count = db.counts.insert(long=payload['longitude'], lat=payload['latitude'], count=payload['wifi'], timestamp=payload['time'])
    db.commit()
    return {
        "inserted": True,
        "count_id": inserted_count.id
    }


@app.get("/devices")
def read_devices():
    """ Get all device ids """
    devices = db.devices.all()
    return devices


@app.get("/devices/{device_id}")
async def read_devices(device_id: str):
    """ Get info for given device id
    """
    device = db.devices.filter(db.devices.id == device_id).one()
    return {"device": device}
    
@app.post("/devices/", status_code=201)
async def create_device(device: model.DeviceModel):
    """ Insert new device into database.

    """
    devices = db.devices.filter(db.devices.id == device.id).all()

    if len(devices) > 0:
        db.delete(devices[0])

    inserted_device = db.devices.insert(id = device.id, data=device.data)
    db.commit()
    return {
        "inserted": True,
        "device_id": inserted_device.id
    }

@app.delete("/devices/{device_id}", status_code=201)
async def create_device(device_id: str):
    """Delete device from database.

    """
    devices = db.devices.filter(db.devices.id == device_id).all()

    if len(devices) > 0:
        db.delete(devices[0])

        db.commit()
        return {
            "removed": True,
            "device_id": device_id
        }
    else:
        return {
            "removed": False,
            "device_id": device_id
        }