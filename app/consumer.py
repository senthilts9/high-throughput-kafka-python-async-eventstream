import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from app.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, DLQ_TOPIC
from app.models import TradeEvent
from app.services import TradeProcessor
from app.utils import setup_json_logger

logger = setup_json_logger("consumer")
_dlq_producer = None

def parse_trade_event(message_bytes: bytes) -> TradeEvent:
    data = json.loads(message_bytes.decode('utf-8'))
    return TradeEvent(**data)

async def send_to_dlq(msg):
    global _dlq_producer
    if _dlq_producer is None:
        _dlq_producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await _dlq_producer.start()

    try:
        await _dlq_producer.send_and_wait(
            topic=DLQ_TOPIC,
            value=msg.value
        )
        logger.warning(f"☠️ DLQ fallback written: offset={msg.offset}")
    except KafkaError as e:
        logger.error(f"🔥 Failed to write to DLQ: {e}")

async def consume_trade_events():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="risk-team-consumer",
        enable_auto_commit=False,
        auto_offset_reset="earliest"
    )
    await consumer.start()
    processor = TradeProcessor()

    try:
        while True:
            messages = await consumer.getmany(timeout_ms=1000)

            for tp, batch in messages.items():
                for msg in batch:
                    try:
                        trade_event = parse_trade_event(msg.value)
                        result = processor.process(trade_event)
                        logger.info(f"✔️ Processed: {result['trade_id']} | Notional={result['notional']}")
                    except Exception as e:
                        logger.error(f"❌ Failed to process msg at offset={msg.offset}: {e}")
                        await send_to_dlq(msg)
                        continue

                last_offset = batch[-1].offset
                await consumer.commit({tp: last_offset + 1})
                logger.info(f"📝 Committed offset: {last_offset + 1} for {tp}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_trade_events())