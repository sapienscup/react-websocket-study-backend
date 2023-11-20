from abc import abstractmethod

from pydantic import BaseModel

from src.constants.contracts import MUST_IMPLEMENT
from src.contracts.base import BaseContract


class TwoFactorProps(BaseModel):
    token: str
    type: str
    username: str
    password: str


class TwoFactorAuthContract(BaseContract):
    @abstractmethod
    def perform(self, props: TwoFactorProps):
        raise NotImplementedError(MUST_IMPLEMENT)
