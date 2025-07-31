import asyncio
import logging
import os
import random
import time
import uuid
from datetime import datetime
from aiokafka import AIOKafkaProducer
from app.models import TradeEvent
from app.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS
from app.utils import setup_json_logger

logger = setup_json_logger("producer")

def generate_trade_event() -> TradeEvent:
    return TradeEvent(
        trade_id=str(uuid.uuid4())[:8],
        symbol="AAPL",
        side="BUY",
        price=198.56,
        quantity=500,
        timestamp=datetime.utcnow().isoformat()
    )

async def send_with_retry(producer: AIOKafkaProducer, topic: str, value: bytes,
                          retries: int = 5, base_delay: float = 0.3, max_delay: float = 5.0):
    attempt = 0
    while True:
        try:
            await producer.send_and_wait(topic=topic, value=value)
            return
        except Exception as e:
            attempt += 1
            if attempt > retries:
                logger.error(f"send_failed: attempts={attempt} error={repr(e)}")
                raise
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            delay = delay * (0.7 + 0.6 * random.random())
            logger.warning(f"send_retry: attempt={attempt} delay={delay:.2f}s error={repr(e)}")
            await asyncio.sleep(delay)

async def send_trade_events():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    HIGH_VOLUME = os.getenv("HIGH_VOLUME", "false").lower() == "true"
    total = 100_000 if HIGH_VOLUME else 10
    delay = 0 if HIGH_VOLUME else 1

    start = time.time()
    try:
        for i in range(total):
            ev = generate_trade_event()
            payload = ev.to_json().encode("utf-8")
            await send_with_retry(producer, KAFKA_TOPIC, payload, retries=5)
            logger.info(f"sent: index={i+1} total={total} trade_id={ev.trade_id}")
            if delay:
                await asyncio.sleep(delay)
    finally:
        await producer.stop()
        elapsed = time.time() - start
        logger.info(f"send_complete: messages={total} elapsed_sec={elapsed:.2f}")

if __name__ == "__main__":
    asyncio.run(send_trade_events())