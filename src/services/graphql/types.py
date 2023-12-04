from typing import Optional

import strawberry

from src.services.blog.post_service import PostService
from src.services.graphql.paging import PaginationWindow


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
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> PaginationWindow[BlogPublication]:
        print(100 * "#")
        print(limit, offset)
        print(100 * "#")

        if limit and offset:
            return PostService().paged(limit, offset)

        return PaginationWindow

    @strawberry.field
    def post(self, postId: Optional[strawberry.ID] or None) -> BlogPublication:
        return PostService().by_id(id)
