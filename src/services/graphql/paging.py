from typing import Generic, List, TypeVar

import strawberry

Item = TypeVar("Item")


@strawberry.type
class PaginationWindow(Generic[Item]):
    items: List[Item] = strawberry.field(description="The list of items in this pagination window.")

    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )
