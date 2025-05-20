import json
import time
import os
import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY non definita. Impostala come variabile d'ambiente.")

LOCATION = 'Verona'
KAFKA_TOPIC = 'weather-data'
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
DELAY_SECONDS = 60
print(f"➡️ Collegamento a Kafka su: {KAFKA_SERVER}")

# ⏳ Aspetta che Kafka sia disponibile
MAX_RETRIES = 60
print("⏳ Attendo che Kafka sia disponibile...")
for attempt in range(MAX_RETRIES):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ Kafka è pronto.")
        break
    except NoBrokersAvailable:
        print(f"❌ Kafka non ancora disponibile (tentativo {attempt + 1}/{MAX_RETRIES})...")
        time.sleep(2)
else:
    raise ConnectionError("⚠️ Impossibile connettersi a Kafka dopo diversi tentativi.")

# 🌦️ Funzione per ottenere dati meteo
def get_current_weather(location):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "location": data['location']['name'],
            "region": data['location']['region'],
            "country": data['location']['country'],
            "lat": data['location']['lat'],
            "lon": data['location']['lon'],
            "local_time": data['location']['localtime'],
            "temp_c": data['current']['temp_c'],
            "humidity": data['current']['humidity'],
            "wind_kph": data['current']['wind_kph'],
            "condition": data['current']['condition']['text'],
            "uv": data['current']['uv']
        }
    except requests.RequestException as e:
        print(f"🌐 Errore durante la richiesta API: {e}")
        return None
    except KeyError as e:
        print(f"❌ Errore nei dati ricevuti: chiave mancante {e}")
        return None

print("🟢 Avvio producer meteo...")

while True:
    weather_data = get_current_weather(LOCATION)
    if weather_data:
        print(f"📤 Inviato a Kafka: {weather_data}")
        producer.send(KAFKA_TOPIC, value=weather_data)
        producer.flush()
    time.sleep(DELAY_SECONDS)









