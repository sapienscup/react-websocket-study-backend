from os import getenv
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_cassandra_host() -> str:
    return getenv("CASSANDRA_USERNAME", "")


def get_cassandra_host() -> str:
    return getenv("CASSANDRA_PASSWORD", "")


def get_cassandra_hosts() -> str:
    return getenv("CASSANDRA_HOSTS", "").split(',')


def get_cassandra_port() -> str:
    return getenv("CASSANDRA_PORT", "")


def get_env_mode() -> str:
    return getenv("ENV_MODE", "")


def get_redis_host() -> str:
    return getenv("REDIS_HOST", "")


def get_redis_port() -> int:
    return int(getenv("REDIS_PORT", 0))


def get_allowed_hosts() -> List:
    return getenv("ALLOWED_HOSTS", "").split(",")


def get_pusher_channel() -> str:
    return getenv("PUSHER_CHANNEL", "")


def get_pusher_event() -> str:
    return getenv("PUSHER_EVENT", "")


def get_openai_api_key() -> str:
    return getenv("OPENAI_API_KEY", "")


def get_gpt_prefix() -> str:
    return getenv("GPT_QUESTION_PREFIX", "")
