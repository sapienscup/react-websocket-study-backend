from src.contracts.base import BaseContract
from src.infra.cass.models.blog import Post
from src.services.todos.fetch import fake_post, fake_posts
from src.infra.envs.envs import get_env_mode
from typing import Optional, List


class PostService(BaseContract):
    def perform(self):
        return fake_posts() if get_env_mode() == "staging" else Post.all()

    def paged(self, limit: Optional[int] or None, offset: Optional[int] or None):
        return fake_posts() if get_env_mode() == "staging" else self._get_pagination_window(Post.all(), limit, offset)

    def by_id(self, id: Optional[int or str] or None):
        return fake_post() if get_env_mode() == "staging" else Post.objects(id=id)

    def _matches(self, item, filters):
        for attr_name, val in filters.items():
            if val not in item[attr_name]:
                return False
        return True

    def _get_pagination_window(
        self,
        dataset: List[Post],
        limit: int,
        offset: int = 0,
        filters: dict[str, str] = {},
    ) -> List[Post]:
        if limit <= 0 or limit > 100:
            raise Exception(f"limit ({limit}) must be between 0-100")

        if filters:
            dataset = list(filter(lambda x: self._matches(x, filters), dataset))

        if offset != 0 and not 0 <= offset < len(dataset):
            raise Exception(f"offset ({offset}) is out of range " f"(0-{len(dataset) - 1})")

        total_items_count = len(dataset)

        items = dataset[offset : offset + limit]

        # items = [ItemType.from_row(x) for x in items]

        return {"items": items, "total_items_count": total_items_count}
