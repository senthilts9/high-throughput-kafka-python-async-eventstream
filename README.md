# 🧠 Kafka + Python Event-Driven Trade Streaming System

## 🚀 Overview

This project simulates a **real-time trade streaming platform** using **Kafka** and **Python's async features (`aiokafka`)**. It demonstrates how to build a **modular**, **observable**, and **fault-tolerant** system for delivering trade events to risk engines or back-office processors.

---

## 📁 Folder Structure

```
kafka-trade-streaming/
├── app/
│   ├── config.py              # Env-based Kafka + DLQ settings
│   ├── models.py              # TradeEvent dataclass
│   ├── producer.py            # Async Kafka producer with retry/backoff
│   ├── consumer.py            # Async Kafka consumer with batch + DLQ
│   ├── services.py            # Business logic (validation + PnL)
│   └── utils.py               # JSON logger setup
├── tests/
│   └── test_services.py       # Pytest unit tests for TradeProcessor
├── requirements.txt
├── run.sh                     # Bootstrap script
├── Dockerfile                 # Python container for producer/consumer
└── README.md
```

---

## 🧠 Architecture Diagram

```
+-------------------+         Kafka Topic        +-------------------------+
| Trade Producer 📨 |  ────────────────────────▶ |  Trade Consumer 🧠       |
| (async Python)    |                           |  - Batch PnL Processor  |
|  - Retry + backoff|                           |  - Manual Offset Commit |
+-------------------+                           |  - DLQ fallback         |
                                                +-----------+-------------+
                                                            |
                                                            ▼
                                                +-------------------------+
                                                |  Dead Letter Queue ☠️   |
                                                |  (Kafka DLQ Topic)      |
                                                +-------------------------+
```

---

## ✅ Features

- ✅ **Async Kafka Producer** using `aiokafka` + `asyncio`
- ✅ **Retry with exponential backoff** and jitter
- ✅ **Async Kafka Consumer** with batch processing (`getmany()`)
- ✅ **Manual offset commit** for **at-least-once delivery**
- ✅ **Dead-letter queue (DLQ)** support for poison messages
- ✅ **PnL + Validation logic** in `TradeProcessor`
- ✅ **Structured JSON logging** for observability
- ✅ **Modular code** with services/utils/models separation
- ✅ **Dockerfile** for containerization
- ✅ **Unit tests** with `pytest`

---

## 🔧 Getting Started

### 🐳 1. Start Kafka via Docker Compose

Use your existing Kafka setup or create a simple one:
```bash
docker-compose up -d
```

### 🧪 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 3. Run Producer

```bash
python app/producer.py
```

Simulate high-volume stream (100K trades):

```bash
HIGH_VOLUME=true python app/producer.py
```

### 📥 4. Run Consumer

```bash
python app/consumer.py
```

It will:
- Batch-consume from Kafka
- Validate + calculate notional
- Commit offset only after success
- Route poison messages to DLQ

---

## 🧪 Running Unit Tests

```bash
pytest -q
```

---

## 🐳 Docker Usage

Build the image:
```bash
docker build -t trade-stream:latest .
```

Run consumer:
```bash
docker run --rm -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 -e KAFKA_TOPIC=trade-events trade-stream:latest
```

Run producer:
```bash
docker run --rm -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 -e KAFKA_TOPIC=trade-events -e HIGH_VOLUME=true trade-stream:latest python app/producer.py
```

---

## 🔁 Delivery Guarantee

- ✅ At-least-once delivery via **manual offset commit**
- ☠️ Messages that fail processing go to **dead-letter-trade-events**
- 🔄 Retries for transient Kafka errors via exponential backoff

---

## 📸 LinkedIn Post Hashtags

When posting your project on LinkedIn, use these:

```
#Kafka #Python #EventDrivenArchitecture #FinTech #AsyncProgramming
#SoftwareEngineering #Microservices #QuantEngineering #BackOffice
#RealTimeData #aiokafka #Docker #TradeLifecycle #PnL #RiskTech
```

---

## 💡 Sample LinkedIn Caption (edit as needed)

> Just built a Kafka + Python async trade streaming system from scratch!  
> - Modular producer/consumer  
> - Real-time validation and notional calc  
> - Retry logic, DLQ fallback, and JSON logs  
> - Ready to scale to 100K+ trades/sec 🚀  
> Perfect for risk teams, back office, or PnL systems.

👉 Check out the repo & demo code on GitHub

---

## 🧠 Future Ideas

- Add Prometheus + Grafana for live metrics
- Write trades to PostgreSQL or ClickHouse
- Add gRPC server or REST API gateway
- Spark-based analytics consumer

---

Built with ❤️ for production-grade event-driven systems in the finance world.