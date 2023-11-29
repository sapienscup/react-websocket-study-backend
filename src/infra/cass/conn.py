from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from src.contracts.base import BaseContract
from src.infra.envs.envs import get_cassandra_host, get_env_mode


class CassConn(BaseContract):
    def __init__(self) -> None:
        self.auth_provider = PlainTextAuthProvider(username="cassandra", password="cassandra")

    def perform(self):
        self.validations()

        hosts = []
        cluster = None
        if get_env_mode() == "development":
            cluster = Cluster(['cassandra'], auth_provider=self.auth_provider)
        else:
            hosts = get_cassandra_host()
            cluster = Cluster(hosts, auth_provider=self.auth_provider)

        return cluster.connect()

    def validations(self) -> bool:
        self._validate_user_id()

    def _validate_user_id(self):
        return True
