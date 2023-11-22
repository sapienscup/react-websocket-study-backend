import asyncio
import json
import random
from time import time

import websockets
from fastapi import WebSocketDisconnect
from starlette.websockets import WebSocket

from src.constants.enums import MessageType
from src.contracts.chat import ChatContract
from src.contracts.connections import ConnectionsManagerContract
from src.services.todos.fetch import generate_chat, wrap_chat_message


class ChatApi(ChatContract):
    def __init__(self, clients: ConnectionsManagerContract) -> None:
        self.clients = clients

    async def perform(self, websocket: WebSocket, choice=MessageType):
        if choice == MessageType.ENTER:
            await self._enter(websocket)

        if choice == MessageType.SEND:
            await self._send(websocket)

        if choice == MessageType.HOW_MUCH:
            await self.clients.connections()

    async def _enter(self, websocket: WebSocket):
        client_host = websocket.client.host

        await websocket.accept()
        self._subscribe(client_host)
        await self._conns(websocket)

        try:
            while True:
                await asyncio.sleep(random.random() * 5)

                await websocket.send_text(json.dumps(generate_chat()))

        except WebSocketDisconnect:
            self._unsubscribe(client_host)
            await self._conns(websocket)
        except websockets.exceptions.ConnectionClosedOK:
            self._unsubscribe(client_host)
            await self._conns(websocket)

    async def _send(self, websocket: WebSocket):
        client_host = websocket.client.host

        await websocket.accept()
        await self._conns(websocket)

        try:
            while True:
                json_data = await websocket.receive_json()

                if json_data:
                    await websocket.send_text(json.dumps(wrap_chat_message(json_data["message"])))

        except WebSocketDisconnect:
            self._unsubscribe(client_host)
            await self._conns(websocket)
        except json.JSONDecodeError:
            await websocket.send_text("WRONG_JSON_FORMAT")
            await self._conns(websocket)
        except websockets.exceptions.ConnectionClosedOK:
            self._unsubscribe(client_host)
            await self._conns(websocket)

    def _subscribe(self, client_host: str):
        self.clients.set(client_host, {"status": "subscribed"})

    def _unsubscribe(self, client_host: str):
        self.clients.set(client_host, {"status": "unsubscribed"})

    def _check(self, client_host: str) -> bool:
        return self.clients.get(client_host)["status"] == "subscribed"

    async def _conns(self, websocket: WebSocket):
        await websocket.send_text(
            json.dumps({"qty": self.clients.connections(), "type": "CONN_QTY"})
        )
