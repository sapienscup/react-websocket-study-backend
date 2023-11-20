from abc import ABC, abstractmethod

from fastapi import Depends, Request
from fastapi.websockets import WebSocket

from src.constants.contracts import MUST_IMPLEMENT


class GraphqlContract(ABC):
    @abstractmethod
    def get_context_value(self, request_or_ws: Request | WebSocket, _data) -> dict:
        raise NotImplementedError(MUST_IMPLEMENT)

    @abstractmethod
    async def handle_graphql_explorer(self, request: Request):
        raise NotImplementedError(MUST_IMPLEMENT)

    @abstractmethod
    async def handle_graphql_query(self, request: Request, data_base_context: Depends):
        raise NotImplementedError(MUST_IMPLEMENT)

    @abstractmethod
    async def graphql_subscriptions(self, websocket: WebSocket, data_base_context: Depends):
        raise NotImplementedError(MUST_IMPLEMENT)
