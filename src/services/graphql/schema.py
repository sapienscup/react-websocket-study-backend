import asyncio
from typing import AsyncGenerator, List

import strawberry

from src.services.graphql.types import Account
from src.dependencies.kafka import get_kafka_producer_instance, get_kafka_consumer_instance


CHAT_CHANNEL = "chat"


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

    @strawberry.subscription
    async def chat_write(self, msg: str) -> AsyncGenerator[int, None]:
        return get_kafka_producer_instance().send(CHAT_CHANNEL, msg)

    @strawberry.subscription
    async def chat_read(self) -> AsyncGenerator[int, None]:
        yield get_kafka_consumer_instance()


@strawberry.type
class Query:
    @strawberry.field
    def user(self, userId: strawberry.ID) -> Account:
        return Account(id=strawberry.ID(userId), name="John", email="abc@bac.com")

    @strawberry.field
    def users(self) -> List[Account]:
        return [Account(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query, subscription=Subscription)
