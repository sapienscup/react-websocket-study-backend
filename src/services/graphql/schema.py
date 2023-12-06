from typing import List

import strawberry

from src.services.graphql.types import Account
from src.services.graphql.subscription import SubscriptionSchema


@strawberry.type
class Query:
    @strawberry.field
    def user(self, userId: strawberry.ID) -> Account:
        if userId == "42c0be29-00d7-4378-9f58-b83bcf1c4d3a":
            return Account(id=strawberry.ID(userId), name="John", email="abc@bac.com")
        return Account()

    @strawberry.field
    def users(self) -> List[Account]:
        return [Account(id=strawberry.ID("1"), name="John", email="abc@bac.com")]


schema = strawberry.Schema(query=Query, subscription=SubscriptionSchema)
