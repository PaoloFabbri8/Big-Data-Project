import json
import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import os
import time
from dotenv import load_dotenv

# Carica variabili da file .env
load_dotenv()

# Configurazioni
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka:9092')
TOPIC = 'weather-data'
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
if not POSTGRES_PASSWORD:
    print("❌ Errore: la variabile d'ambiente POSTGRES_PASSWORD non è definita!")
    exit(1)

# Connessione al database PostgreSQL
try: 
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'weatherdb'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=POSTGRES_PASSWORD
    )
except Exception as e:
    print(f"❌ Errore durante la connessione al database PostgreSQL: {e}")
    exit(1)

cursor = conn.cursor()

# Creazione tabella se non esiste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        location TEXT,
        region TEXT,
        country TEXT,
        lat REAL,
        lon REAL,
        local_time TEXT,
        temp_c REAL,
        humidity INT,
        wind_kph REAL,
        condition TEXT,
        uv REAL
    );
''')
conn.commit()

# Retry loop per Kafka
max_retries = 10
retry_delay = 5  # secondi

for attempt in range(max_retries):
    try:
        print(f"🔄 Tentativo di connessione a Kafka ({attempt+1}/{max_retries})...")
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='weather-group'
        )
        print(f"✅ Connesso a Kafka. In ascolto sul topic '{TOPIC}'...")
        break
    except NoBrokersAvailable:
        print("⚠️ Kafka non disponibile, nuovo tentativo tra 5 secondi...")
        time.sleep(retry_delay)
else:
    print("❌ Errore: impossibile connettersi a Kafka dopo vari tentativi. Esco.")
    exit(1)

# Lettura dei messaggi Kafka
for message in consumer:
    data = message.value
    print(f"📨 Ricevuto: {data}")
    cursor.execute('''
        INSERT INTO weather_data (
            location, region, country, lat, lon, local_time,
            temp_c, humidity, wind_kph, condition, uv
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data['location'], data['region'], data['country'],
        data['lat'], data['lon'], data['local_time'],
        data['temp_c'], data['humidity'], data['wind_kph'],
        data['condition'], data['uv']
    ))
    conn.commit()