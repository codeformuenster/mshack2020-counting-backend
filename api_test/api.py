from fastapi import FastAPI, HTTPException
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
    """ Get all counts """
    counts = db.counts.all()
    return {"counts": counts}


@app.get("/counts/{count_id}")
def read_count(count_id: int) -> model.Count:
    """Read count for a given ID.

    Args:

        count_id (int): ID of count to be read

    Returns:

        Count: Count entry
    """
    count = db.counts.filter(db.counts.id == count_id).one()
    return {"count": count}


@app.post("/counts/", status_code=201)
async def create_count(count: model.CountParameter):
    """Insert new count into database.

    Example JSON body:

    Key `data` is optional.

    ```
    {
        "count": 10,
        "timestamp": "2020-09-26T09:10:11",
        "device_id": "counter-a"
        "data": {
            "key-a": "value-a",
            "whatever": "you want"
        }
    }
    ```
    """

    # try to find the device based on the device_id
    devices = db.devices.filter(db.devices.id == count.device_id).all()
    if len(devices) == 0:
        raise HTTPException(status_code=400, detail="Unknown device")

    inserted_count = db.counts.insert(
        count=count.count,
        timestamp=count.timestamp,
        device_id=count.device_id,
        data=count.data,
    )

    db.commit()
    return {"inserted": True, "count_id": inserted_count.id}


@app.post("/ttn_pax_counts/", status_code=201)
async def create_count(count: model.TTNHTTPIntegrationParameter):
    """
    Endpoint for TTN HTTP integration sending pax counter data.

    Reads some fields of the TTN HTTP integrations json fields.

    """
    data = count.dict()
    payload = data["payload_fields"]
    meta = data["metadata"]
    inserted_count = db.counts.insert(
        count=payload["wifi"],
        timestamp=meta["time"],
        device_id=data["dev_id"],
        data=payload,
    )
    db.commit()
    return {"inserted": True, "count_id": inserted_count.id}


@app.get("/devices")
def read_devices():
    """ Get all devices """
    devices = db.devices.all()
    return devices


@app.get("/devices/{device_id}")
async def read_device(device_id: str):
    """Get info for given device id"""
    device = db.devices.filter(db.devices.id == device_id).one()
    return {"device": device}


@app.post("/devices/", status_code=201)
async def create_device(device: model.DeviceParameter):
    """Insert new device into database.

    Example JSON:

    Field `data` is optional.

    ```
    {
        "id": "my-device",
        "lat": 51.96,
        "lon": 7.62,
        "data": {
            "bassmachine": "5000 Watt"
        }
    }
    ```

    """
    devices = db.devices.filter(db.devices.id == device.id).all()

    if len(devices) > 0:
        raise HTTPException(status_code=400, detail="Device already exists")

    inserted_device = db.devices.insert(
        id=device.id, lat=device.lat, lon=device.lon, data=device.data
    )
    db.commit()
    return {"inserted": True, "device_id": inserted_device.id}


@app.delete("/devices/{device_id}", status_code=200)
async def delete_device(device_id: str):
    """Delete device from database."""
    devices = db.devices.filter(db.devices.id == device_id).all()

    if len(devices) > 0:
        db.delete(devices[0])

        db.commit()
        return {"removed": True, "device_id": device_id}
    else:
        raise HTTPException(status_code=400, detail="Unknown device_id")
