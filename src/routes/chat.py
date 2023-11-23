import http

import pusher
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

from src.constants.enums import MessageType
from src.constants.responses import INTERNAL_ERROR
from src.infra.ws.conn_manager import DictConnMan
from src.services.chat.chat_api import ChatApi, PublishChatApi

router = APIRouter(
    prefix="/chat",
    tags=["Chats Socket"],
    responses={
        http.HTTPStatus.UNAUTHORIZED.value: {
            "message": "Auth failed",
        },
        http.HTTPStatus.INTERNAL_SERVER_ERROR.value: {"message": INTERNAL_ERROR},
    },
)

connManager = DictConnMan()

pusher_client = pusher.Pusher(
    app_id="1712845",
    key="a08a9b5076a727a59ad8",
    secret="09f5f31aeaa8ea303dc2",
    cluster="mt1",
    ssl=True,
)


class Item(BaseModel):
    message: str


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ChatApi(connManager, pusher_client).perform(websocket, MessageType.ENTER)


@router.post("/send")
def send_msg_to_chat_channel(item: Item) -> http.HTTPStatus:
    return PublishChatApi(pusher_client).perform(item.message, MessageType.SEND)


@router.websocket("/ws/send")
async def websocket_endpoint(websocket: WebSocket):
    await ChatApi(DictConnMan(), pusher_client).perform(websocket, MessageType.SEND)
