from os import getenv
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_kafka_host() -> str:
    return getenv("KAFKA_HOST", "")


def get_kafka_port() -> str:
    return getenv("KAFKA_PORT", "")


def get_kafka_topic() -> str:
    return getenv("KAFKA_TOPIC", "")


def get_kafka_group_id() -> str:
    return getenv("KAFKA_GROUP_ID", "")


def get_mongo_host() -> str:
    return getenv("MONGO_HOST", "")


def get_mongo_port() -> str:
    return getenv("MONGO_PORT", "")


def get_mongo_username() -> str:
    return getenv("MONGO_USERNAME", "")


def get_mongo_password() -> str:
    return getenv("MONGO_PASSWORD", "")


def get_cassandra_username() -> str:
    return getenv("CASSANDRA_USERNAME", "")


def get_cassandra_password() -> str:
    return getenv("CASSANDRA_PASSWORD", "")


def get_cassandra_hosts() -> str:
    return getenv("CASSANDRA_HOSTS", "").split(",")


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
