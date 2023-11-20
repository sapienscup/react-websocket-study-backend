from http import HTTPStatus

from fastapi import APIRouter

from src.constants.responses import INTERNAL_ERROR
from src.dependencies.two_factor import two_factor_dependency
from src.services.health_check.health_check import HealthCheck

router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"message": INTERNAL_ERROR},
    },
)


@router.get(
    "/",
    tags=["Health Check"],
    status_code=HTTPStatus.OK.value,
    summary="Health Check",
    description="Server answering normally",
    responses={
        HTTPStatus.OK.value: {
            "message": "Server is health",
        },
    },
    dependencies=[two_factor_dependency],
)
async def health_check():
    return HealthCheck().perform()
