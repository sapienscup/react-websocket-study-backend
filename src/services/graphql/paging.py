from typing import Generic, List, TypeVar

import strawberry

T = TypeVar("T")


@strawberry.type
class PaginationWindow(Generic[T]):
    items: List[T] = strawberry.field(description="The list of items in this pagination window.")

    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )
