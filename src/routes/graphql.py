from http import HTTPStatus

from fastapi import APIRouter, Request
from fastapi.websockets import WebSocket

from src.constants.responses import INTERNAL_ERROR
from src.dependencies.db import get_database_session_dependency
from src.services.graphql.graphql import GraphqlService

router = APIRouter(
    prefix="/graphql",
    tags=["GraphQl"],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"message": INTERNAL_ERROR},
    },
)


@router.get("/")
@router.options("/")
async def handle_graphql_explorer(request: Request):
    return await GraphqlService().handle_graphql_explorer(request)


@router.post("/")
async def handle_graphql_query(
    request: Request,
    data_base_context=get_database_session_dependency,
):
    request.scope["db"] = data_base_context
    return await GraphqlService().handle_graphql_query(request)


@router.websocket("/")
async def graphql_subscriptions(
    websocket: WebSocket,
    data_base_context=get_database_session_dependency,
):
    await GraphqlService().graphql_subscriptions(websocket, data_base_context)
