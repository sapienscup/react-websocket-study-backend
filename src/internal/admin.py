from http import HTTPStatus

from fastapi import APIRouter

from src.constants.responses import INTERNAL_ERROR
from src.dependencies.standard_tokens import get_token_header_dependency
from src.dependencies.two_factor import two_factor_dependency

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[get_token_header_dependency],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        # pylint: disable=no-member
        HTTPStatus.IM_A_TEAPOT.value: {
            "message": "I'm a teapot"
        },
        # pylint: enable=no-member
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "message": INTERNAL_ERROR
        },
    },
)


@router.get(
    "/",
    tags=["Admin"],
    status_code=HTTPStatus.OK.value,
    summary="Admin",
    description="Fetch admin permissions",
    responses={
        HTTPStatus.OK.value: {
            "message": "Admin permissions",
        },
    },
    dependencies=[two_factor_dependency],
)
async def admin_permissions():
    return {}
