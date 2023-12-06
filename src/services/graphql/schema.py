import fastapi.responses
import http
import json
import signal
import time
import uuid
from typing import AsyncGenerator, List

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
from src.services.graphql.types import Account

CHAT_CHANNEL = "chat"
MIN_TIMEOUT = 5


class ChatException(BaseException):
    pass


def handler(signum, frame):
    raise ChatException("EndOfStream")


signal.signal(signal.SIGALRM, handler)


@strawberry.type
class Subscription:
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
                yield f"topic={msg.topic}: key={msg.key.decode('utf-8')}, msg={json.loads(msg.value)}, timestamp={msg.timestamp}"
        finally:
            await consumer.stop()


@strawberry.type
class Query:
    @strawberry.field
    def user(self, userId: strawberry.ID) -> Account:
        return Account(id=strawberry.ID(userId), name="John", email="abc@bac.com")

    @strawberry.field
    def users(self) -> List[Account]:
        return [Account(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query, subscription=Subscription)
