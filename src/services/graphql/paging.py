from typing import Generic, List, TypeVar

import strawberry

Model = TypeVar("Model")


@strawberry.type
class PaginationWindow(Generic[Model]):
    items: List[Model] = strawberry.field(description="The list of items in this pagination window.")

    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )
