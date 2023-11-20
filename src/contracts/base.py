from abc import ABC, abstractmethod

from src.constants.contracts import MUST_IMPLEMENT


class BaseContract(ABC):
    @abstractmethod
    def perform(self):
        raise NotImplementedError(MUST_IMPLEMENT)


class AsyncBaseContract(ABC):
    @abstractmethod
    async def perform(self):
        raise NotImplementedError(MUST_IMPLEMENT)
