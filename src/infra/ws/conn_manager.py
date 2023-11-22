import json, redis, uuid

from src.contracts.connections import ConnectionsManagerContract
from src.infra.envs.envs import get_redis_host, get_redis_port


class DictConnMan(ConnectionsManagerContract):
    def __init__(self):
        self.kv: dict[str, dict] = {}

    def set(self, key: any, value: any):
        self.kv[f"{uuid.uuid4()}-{key}"] = value

    def get(self, key: any):
        self.kv.get(key)

    def connections(self) -> int:
        return list(self.kv.keys())


class RedisConnManager(ConnectionsManagerContract):
    def __init__(self):
        self.kv = redis.Redis(
            host=get_redis_host(), port=get_redis_port(), decode_responses=True, db=0
        )

    def set(self, key: any, value: any):
        self.kv.set(f"{uuid.uuid4()}-{key}", json.dumps(value))

    def get(self, key: any):
        return json.loads(self.kv.get(key))

    def connections(self):
        return len(self.kv.keys())
