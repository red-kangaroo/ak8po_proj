# Weather frontend
#
# Build with:
#   docker build -t ak8po_frontend:<version>
FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD ./weather /app/
WORKDIR /app

RUN pip install --upgrade --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
