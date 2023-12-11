from typing import Any, List, Optional

from src.contracts.base import BaseContract
from src.infra.cass.models.blog import Post
from src.infra.envs.envs import get_env_mode
from src.services.todos.fetch import fake_post, fake_posts
from src.services.graphql.paging import PaginationWindow


class PostService(BaseContract):
    def perform(self):
        return fake_posts() if get_env_mode() == "staging" else Post.all()

    def paged(self, limit: Optional[int] or None, offset: Optional[int] or None):
        return (
            PaginationWindow(**{"items": fake_posts(), "total_items_count": 100})
            if get_env_mode() == "staging"
            else self._get_pagination_window(Post.all(), limit, offset)
        )

    def by_id(self, id: Optional[int or str] or None):
        if get_env_mode() == "staging":
            return fake_post()

        if post := Post.objects(id=id):
            return post.get()

    def _matches(self, item: any, filters: dict):
        for attr_name, val in filters.items():
            if val not in item[attr_name]:
                return False
        return True

    def _get_pagination_window(
        self,
        dataset: List[Any],
        limit: int,
        offset: int = 0,
        filters: dict[str, str] = {},
    ) -> PaginationWindow:
        if limit <= 0 or limit > 100:
            raise Exception(f"limit ({limit}) must be between 0-100")

        if filters:
            dataset = list(filter(lambda x: self._matches(x, filters), dataset))

        if offset != 0 and not 0 <= offset < len(dataset):
            raise Exception(f"offset ({offset}) is out of range " f"(0-{len(dataset) - 1})")

        total_items_count = len(dataset)

        items: List[Post] = dataset[offset : offset + limit]

        return PaginationWindow(**{"items": items, "total_items_count": total_items_count})
