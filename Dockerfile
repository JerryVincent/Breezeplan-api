FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}
