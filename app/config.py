import os

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "trade-events")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
DLQ_TOPIC = os.getenv("DLQ_TOPIC", "dead-letter-trade-events")