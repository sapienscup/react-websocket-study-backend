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
    def posts(self, limit: Optional[int] or None, offset: Optional[int] or None) -> PaginationWindow[BlogPublication]:
        if limit and offset:
            return PostService().paged(limit, offset)
        return PostService().perform()

    def post(self, id: Optional[strawberry.ID] or None) -> BlogPublication:
        return PostService().by_id(id) if id else PostService().perform(id)
