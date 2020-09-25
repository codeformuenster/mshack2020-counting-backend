FROM python:3.8-slim

EXPOSE 8080

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY setup.py /app/setup.py
COPY ./scripts /app/scripts
COPY ./api_test /app/api_test
COPY ./laser_import /app/laser_import
RUN pip install .

CMD ["uvicorn", "api_test.api:app", "--host=0.0.0.0", "--port=8080"]
