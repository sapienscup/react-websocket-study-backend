import g4f

from src.contracts.base import BaseContract
from src.infra.envs.envs import get_gpt_prefix

g4f.debug.logging = True
g4f.check_version = False
print(g4f.version)
print(g4f.Provider.Ails.params)


class ChatAssistant(BaseContract):
    def perform(self, msg: str):
        rsp = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[
                {
                    "role": "user",
                    "content": f"{get_gpt_prefix()} {msg}",
                }
            ],
        )

        return self._parse(rsp)

    def _parse(self, rsp: str):
        return rsp.split('\n')[-1]
