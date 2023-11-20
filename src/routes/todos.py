from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.constants.responses import INTERNAL_ERROR
from src.dependencies.two_factor import two_factor_dependency
from src.services.todos.fetch import TodosFetchService
from src.services.two_factor.auth import TwoFactorAuth

router = APIRouter(
    prefix="/todos",
    tags=["User to dos"],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"message": INTERNAL_ERROR},
    },
)


@router.get(
    "/",
    tags=["User to dos"],
    status_code=HTTPStatus.OK.value,
    summary="Fetch to dos",
    description="Show to dos",
    responses={
        HTTPStatus.OK.value: {
            "message": "Fetched to dos of the user",
        },
    },
    dependencies=[two_factor_dependency],
)
async def fetch_todos():
    return TodosFetchService().perform()
