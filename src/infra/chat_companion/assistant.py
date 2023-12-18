from src.contracts.base import BaseContract


class ChatAssistant(BaseContract):
    def perform(self, msg: str):
        return "Chat completions inactivated"
