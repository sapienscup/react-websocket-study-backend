from http import HTTPStatus

from fastapi import APIRouter, WebSocket

from src.constants.enums import MessageType
from src.constants.responses import INTERNAL_ERROR
from src.infra.ws.conn_manager import DictConnMan
from src.services.chat.chat_api import ChatApi

router = APIRouter(
    prefix="/chat",
    tags=["Chats Socket"],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"message": INTERNAL_ERROR},
    },
)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ChatApi(DictConnMan()).perform(websocket, MessageType.ENTER)


@router.websocket("/ws/send")
async def websocket_endpoint(websocket: WebSocket):
    await ChatApi(DictConnMan()).perform(websocket, MessageType.SEND)
