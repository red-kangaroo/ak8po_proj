# Weather forecast
#
# Build with:
#   docker build -t ak8po_weather:<version>
FROM python:3.8-slim

ADD . /

RUN pip install --upgrade --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "weather.py" ]
