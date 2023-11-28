from typing import List

import strawberry
from src.services.blog.post_service import PostService


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
    def posts(self) -> List[Post]:
        return PostService().perform()


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=strawberry.ID("1"), name="John", email="abc@bac.com")

    @strawberry.field
    def users(self) -> List[User]:
        return [User(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query)
