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
async def create_count(long: float, lat: float, count: float): #-> Optional
    """ Insert new count into database.

    Args:

        long (float): Longitude of count

        lat (float): Latitude of count

        count (float): Count value
    """
    count = db.counts.insert(long=long, lat=lat, count=count)
    db.commit()
    return {
        "inserted": True,
        "count_id": count.id
    }
