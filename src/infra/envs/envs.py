from os import getenv
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_cassandra_host() -> str:
    return getenv("CASS_USER", "")


def get_cassandra_host() -> str:
    return getenv("CASS_PASS", "")


def get_cassandra_host() -> str:
    return getenv("CASS_HOST", "")


def get_cassandra_port() -> str:
    return getenv("CASS_PORT", "")


def get_env_mode() -> str:
    return getenv("MODE", "")


def get_redis_host() -> str:
    return getenv("REDIS_HOST", "")


def get_redis_port() -> int:
    return int(getenv("REDIS_PORT", 0))


def get_allowed_hosts() -> List:
    return getenv("ALLOWED_HOSTS", "").split(",")
