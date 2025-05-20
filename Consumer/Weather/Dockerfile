FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Aspetta Kafka e Postgres prima di partire con Consumer.py
CMD ["sh", "-c", "python wait_for_kafka.py kafka:9092 && python wait_for_postgres.py postgres:5432 && python Consumer.py"]