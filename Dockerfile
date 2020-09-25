FROM python:3.7

EXPOSE 80

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY setup.py /app/setup.py
COPY ./scripts /app/scripts
COPY ./api_test /app/api_test
RUN pip install .
