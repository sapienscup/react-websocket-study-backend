from typing import Generic, List, TypeVar

import strawberry

Agnostic = TypeVar("Agnostic")


@strawberry.type
class PaginationWindow(Generic[Agnostic]):
    items: List[Agnostic] = strawberry.field(description="The list of items in this pagination window.")

    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )
