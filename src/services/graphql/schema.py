import asyncio
from typing import Any, Optional, AsyncGenerator, List

import strawberry

from src.services.blog.post_service import PostService


@strawberry.type
class Paged:
    items: strawberry
    total_items_count: int


@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    body: str
    author: str
    created_at: str
    updated_at: str


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    def posts(self, limit: Optional[int] or None, offset: Optional[int] or None) -> Paged:
        if limit and offset:
            return Paged(**PostService().paged(limit, offset))
        return PostService().perform()

    def post(self, id: Optional[strawberry.ID] or None) -> Post:
        return PostService().by_id(id) if id else PostService().perform(id)

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
