from abc import ABC, abstractmethod

from src.constants.contracts import MUST_IMPLEMENT


class ConnectionsManagerContract(ABC):
    @abstractmethod
    def get(self, key: any):
        raise NotImplemented(MUST_IMPLEMENT)

    @abstractmethod
    def set(self, key: any, value: any):
        raise NotImplemented(MUST_IMPLEMENT)
