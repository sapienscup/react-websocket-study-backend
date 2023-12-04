import asyncio
from typing import AsyncGenerator, List

import strawberry

from src.services.graphql.types import User


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return User(id=strawberry.ID(id), name="John", email="abc@bac.com")

    @strawberry.field
    def users(self) -> List[User]:
        return [User(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query, subscription=Subscription)
