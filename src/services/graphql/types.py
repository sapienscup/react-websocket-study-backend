from typing import Optional

import strawberry

from src.services.blog.post_service import PostService
from src.services.graphql.paging import PaginationWindow
from src.infra.exceptions.graphql import GraphqlServiceException


@strawberry.type
class Profile:
    name: str


@strawberry.type
class BlogPublication:
    id: strawberry.ID
    title: str
    body: str
    user: Profile
    created_at: str
    updated_at: str


@strawberry.type
class Account:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    def posts(
        self, limit: int, offset: int) -> PaginationWindow[BlogPublication]:
        if limit and offset:
            return PostService().paged(limit, offset)

    @strawberry.field
    def post(self, postId: Optional[strawberry.ID] or None) -> BlogPublication:
        return PostService().by_id(postId)
