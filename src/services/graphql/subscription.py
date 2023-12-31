import json
import signal
import time
import uuid
from typing import AsyncGenerator

import strawberry
from aiokafka import AIOKafkaConsumer

from src.dependencies.kafka import get_kafka_producer_instance
from src.infra.envs.envs import (
    get_env_mode,
    get_kafka_group_id,
    get_kafka_host,
    get_kafka_port,
    get_kafka_topic,
)
from src.infra.exceptions.graphql import ChatException

CHAT_CHANNEL = "chat"
MIN_TIMEOUT = 5


def handler(signum, frame):
    raise ChatException("EndOfStream")


signal.signal(signal.SIGALRM, handler)


@strawberry.type
class SubscriptionSchema:
    @strawberry.subscription
    async def chat_write(self, msg: str) -> AsyncGenerator[str, None]:
        if get_env_mode() == "staging":
            yield f"Heard: {msg} (staging don't operate with kafka)"
            return

        get_kafka_producer_instance().send(
            topic=CHAT_CHANNEL,
            key=bytes(str(uuid.uuid4()), "utf-8"),
            value=msg,
            timestamp_ms=int(time.time()),
        )

        yield f"Heard: {msg}"

    @strawberry.subscription
    async def chat_read(self) -> AsyncGenerator[str, None]:
        if get_env_mode() == "staging":
            yield "CONSUMED"
            return

        consumer = AIOKafkaConsumer(
            get_kafka_topic(),
            bootstrap_servers=f"{get_kafka_host()}:{get_kafka_port()}",
            group_id=get_kafka_group_id(),
        )
        await consumer.start()
        try:
            async for msg in consumer:
                rsp_item = {
                    "topic": msg.topic,
                    "key": msg.key.decode("utf-8"),
                    "msg": json.loads(msg.value),
                    "timestamp": msg.timestamp,
                }
                yield json.dumps(rsp_item)
        finally:
            await consumer.stop()
