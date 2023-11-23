import asyncio
import http
import json
import random
from json import JSONDecodeError

import pusher
from fastapi import WebSocketDisconnect
from starlette.websockets import WebSocket
from websockets.exceptions import ConnectionClosedOK

from src.constants.enums import MessageType
from src.contracts.base import BaseContract
from src.contracts.chat import ChatContract
from src.contracts.connections import ConnectionsManagerContract
from src.services.todos.fetch import generate_chat, wrap_chat_message

PUSHER_CHANNEL = "my-channel"
MY_EVENT = "my-event"


class PublishChatApi(BaseContract):
    def __init__(self, pusher: pusher.Pusher) -> None:
        self.pusher = pusher

    def perform(self, message: str, choice) -> dict:
        if choice == MessageType.SEND:
            return self._publish(message)

    def _publish(self, message: str) -> dict:
        msg = wrap_chat_message(message)

        dumped_msg = json.dumps(msg)

        self.pusher.trigger(PUSHER_CHANNEL, MY_EVENT, dumped_msg)

        return http.HTTPStatus.NO_CONTENT

class ChatApi(ChatContract):
    def __init__(self, clients: ConnectionsManagerContract, pusher: pusher.Pusher) -> None:
        self.clients = clients
        self.pusher = pusher

    async def perform(self, websocket: WebSocket, choice=MessageType):
        if choice == MessageType.ENTER:
            await self._enter(websocket)

        if choice == MessageType.SEND:
            await self._send(websocket)

        if choice == MessageType.HOW_MUCH:
            await self.clients.connections()

    async def _enter(self, websocket: WebSocket):
        conn_key = websocket.client.port

        await websocket.accept()
        self._subscribe(conn_key)

        try:
            while True:
                await asyncio.sleep(random.random() * 5)

                msg = generate_chat()

                dumped_msg = json.dumps(msg)

                await websocket.send_text(dumped_msg)

                await self._conns(websocket)

                self.pusher.trigger(PUSHER_CHANNEL, MY_EVENT, dumped_msg)

        except WebSocketDisconnect:
            self._unsubscribe(conn_key)
        except ConnectionClosedOK:
            self._unsubscribe(conn_key)

    async def _send(self, websocket: WebSocket):
        conn_key = websocket.client.port

        await websocket.accept()

        try:
            while True:
                json_data = await websocket.receive_json()

                if json_data:
                    msg = wrap_chat_message(json_data["message"])

                    dumped_msg = json.dumps(msg)

                    await websocket.send_text(dumped_msg)

                    self.pusher.trigger(PUSHER_CHANNEL, MY_EVENT, dumped_msg)

        except WebSocketDisconnect:
            self._unsubscribe(conn_key)
        except JSONDecodeError:
            await websocket.send_text("WRONG_JSON_FORMAT")
        except ConnectionClosedOK:
            self._unsubscribe(conn_key)

    def _subscribe(self, key: str):
        self.clients.set(key, {"status": "subscribed"})

    def _unsubscribe(self, key: str):
        self.clients.unset(key)

    def _check(self, key: str) -> bool:
        return self.clients.get(key)["status"] == "subscribed"

    async def _conns(self, websocket: WebSocket):
        await websocket.send_text(
            json.dumps({"qty": self.clients.connections(), "type": "CONN_QTY"})
        )
