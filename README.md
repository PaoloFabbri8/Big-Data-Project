# 🌾 Crop Disease Prediction and Alert System

## 📚 Assignment

**Crop Disease Prediction and Alert System**

Design and prototype a big data system for real-time detection and prediction of crop diseases. Aggregate data from on-field IoT sensors (temperature, humidity, soil pH), drone imagery, and local weather information. Use machine learning in (or on top of) Spark or Flink to detect anomalies indicative of pests or diseases. Generate early warnings for farmers and suggest targeted interventions (pesticide usage, irrigation adjustments). Integrate a dashboard that visually maps high-risk areas, improving food security and reducing crop losses.

## 🚀 Project Overview

This system:
- Ingests data from IoT sensors and weather APIs  
- Streams the data through Kafka topics  
- Consumes and stores the data in PostgreSQL  
- Can apply anomaly detection (future)  
- Will expose alerts and visualization (future dashboard)  

## 📦 Architecture


## Environment Configuration

This project requires some environment variables to run properly.  
To keep your sensitive data safe, these variables are stored in a `.env` file that **is not tracked by Git**.

### 1. Create your `.env` file

After cloning the repository, create a `.env` file by copying the provided example:

```bash
cp .env.example .env
```

### 2. Edit your .env file
Open .env with a text editor and insert your own values. For example:

```bash
API_KEY=your_api_key_here
KAFKA_SERVER=kafka:9092
POSTGRES_HOST=postgres
POSTGRES_DB=weatherdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
```

### 3. How to get your API Key

- Go to WeatherAPI (or your specific API provider)
- Create a free account
- Navigate to your dashboard and copy your API key
- Paste it in the API_KEY field of your .env

### 4. Keep your .env secure

- Do not commit .env to GitHub — it is included in .gitignore to avoid exposing sensitive data publicly.
- Share .env.example as a template for collaborators.
- Each collaborator must create their own .env locally.