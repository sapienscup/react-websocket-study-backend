import time
import uuid
import signal
from typing import AsyncGenerator, List

import strawberry

from src.dependencies.kafka import get_kafka_consumer_instance, get_kafka_producer_instance, consume
from src.infra.envs.envs import get_env_mode
from src.services.graphql.types import Account

CHAT_CHANNEL = "chat"
MIN_TIMEOUT = 5

def handler(signum, frame):
    raise Exception

signal.signal(signal.SIGALRM, handler)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def chat_write(self, msg: str) -> AsyncGenerator[str, None]:
        if get_env_mode() == "staging":
            yield "PRODUCED"
            return

        get_kafka_producer_instance().send(
            topic=CHAT_CHANNEL,
            key=bytes(str(uuid.uuid4()), "utf-8"),
            value=msg,
            timestamp_ms=int(time.time()),
        )

        yield "PRODUCED"

    @strawberry.subscription
    async def chat_read(self) -> AsyncGenerator[str, None]:
        if get_env_mode() == "staging":
            yield "CONSUMED"
            return

        signal.alarm(MIN_TIMEOUT)

        consumer = get_kafka_consumer_instance()

        for message in consumer:
            yield f'{message.topic}: key={message.key} value={message.value.decode("utf-8")}'

@strawberry.type
class Query:
    @strawberry.field
    def user(self, userId: strawberry.ID) -> Account:
        return Account(id=strawberry.ID(userId), name="John", email="abc@bac.com")

    @strawberry.field
    def users(self) -> List[Account]:
        return [Account(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query, subscription=Subscription)
