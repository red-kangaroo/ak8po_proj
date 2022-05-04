# Weather frontend
#
# Build with:
#   docker build -t ak8po_frontend:<version>
FROM python:3.8-slim

ADD . /

RUN pip install --upgrade --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
