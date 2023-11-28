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
from src.infra.chat_companion.assistant import ChatAssistant
from src.infra.envs.envs import get_pusher_channel, get_pusher_event
from src.services.todos.fetch import generate_chat, wrap_chat_message


class PublishChatApi(BaseContract):
    def __init__(self, pusher: pusher.Pusher, gptPlugin: ChatAssistant) -> None:
        self.pusher = pusher
        self.gptPlugin = gptPlugin

    def perform(self, message: str, choice) -> None:
        if choice == MessageType.SEND:
            return self._publish(message)

    def _publish(self, message: str) -> None:
        self._extracted_from__publish_9("Você", message)
        if gpt_answer := self._check_msg_is_a_question_to_gpt(message):
            self._extracted_from__publish_9("GPT", gpt_answer)
        return http.HTTPStatus.NO_CONTENT

    def _extracted_from__publish_9(self, arg0, arg1) -> None:
        wrapped_msg = wrap_chat_message(arg0, arg1)
        dumped_gpt_answer = json.dumps(wrapped_msg)
        self.pusher.trigger(get_pusher_channel(), get_pusher_event(), dumped_gpt_answer)

    def _check_msg_is_a_question_to_gpt(self, msg: str) -> str:
        return self.gptPlugin.perform(msg) if msg.endswith("?") else ""


class WebsocketChatApi(ChatContract):
    def __init__(self, clients: ConnectionsManagerContract, pusher: pusher.Pusher) -> None:
        self.clients = clients
        self.pusher = pusher

    async def perform(self, websocket: WebSocket, choice=MessageType):
        if choice == MessageType.ENTER:
            await self._enter(websocket)

        if choice == MessageType.SEND:
            await self._send(websocket)

        if choice == MessageType.LOGIN:
            return http.HTTPStatus.NO_CONTENT

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

                self.pusher.trigger(get_pusher_channel(), get_pusher_event(), dumped_msg)

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

                    self.pusher.trigger(get_pusher_channel(), get_pusher_event(), dumped_msg)

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
