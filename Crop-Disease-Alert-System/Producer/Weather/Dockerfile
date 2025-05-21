FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Aspetta che Kafka sia disponibile prima di partire con Producer.py
CMD ["sh", "-c", "python wait_for_kafka.py kafka:9092 && python Producer.py"]