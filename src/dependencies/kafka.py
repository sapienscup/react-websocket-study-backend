import json

from kafka import KafkaProducer
from kafka import TopicPartition
from kafka import KafkaConsumer

from src.infra.envs.envs import get_kafka_group_id, get_kafka_host, get_kafka_port, get_kafka_topic


def get_kafka_producer_instance():
    return KafkaProducer(
        bootstrap_servers=f"{get_kafka_host()}:{get_kafka_port()}",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def get_kafka_consumer_instance():
    consumer = KafkaConsumer(
        get_kafka_topic(),
        group_id=get_kafka_group_id(),
        bootstrap_servers=f"{get_kafka_host()}:{get_kafka_port()}",
    )
    for message in consumer:
        print(
            "%s:%d:%d: key=%s value=%s"
            % (message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8'))
        )