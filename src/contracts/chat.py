from abc import ABC, abstractmethod

from fastapi import Request
from starlette.websockets import WebSocket

from src.constants.contracts import MUST_IMPLEMENT
from src.contracts.base import AsyncBaseContract


class ChatContract(AsyncBaseContract):
    pass
