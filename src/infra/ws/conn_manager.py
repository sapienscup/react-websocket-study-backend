import json

import redis

from src.contracts.connections import ConnectionsManagerContract
from src.infra.envs.envs import get_redis_host, get_redis_port


class DictConnMan(ConnectionsManagerContract):
    def __init__(self):
        self.r: dict[str, dict] = {}

    def set(self, key: any, value: any):
        self.r[key] = value

    def get(self, key: any):
        self.r.get(key)


class RedisConnManager(ConnectionsManagerContract):
    def __init__(self):
        self.r = redis.Redis(
            host=get_redis_host(), port=get_redis_port(), decode_responses=True, db=0
        )

    def set(self, key: any, value: any):
        self.r.set(key, json.dumps(value))

    def get(self, key: any):
        json.loads(self.r.get(key))
