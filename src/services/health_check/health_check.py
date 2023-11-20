from http import HTTPStatus

from src.contracts.health import HealthCheckContract


class HealthCheck(HealthCheckContract):
    def perform(self):
        return HTTPStatus.OK
