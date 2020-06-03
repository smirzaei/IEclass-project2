import logging

from asyncio.events import AbstractEventLoop
from typing import Callable, Any
from socket import socket
from textwrap import dedent

logger = logging.getLogger(__name__)
from uuid import uuid4

class Connection:
    def __init__(
        self,
        event_loop: AbstractEventLoop,
        sock: socket,
        address: Any,
        on_msg: Callable[[str, str], None]
    ) -> None:
        self.id = uuid4().hex
        self.sock = sock
        self.event_loop = event_loop
        self.address = address
        self.on_msg = on_msg

        welcome_msg = dedent("""
            ===============================================
            Hello!
            You are now connected to the chat server.
            Your messages will be broadcast to other users.
            ===============================================
        """)

        event_loop.create_task(self.listen_for_msgs())
        event_loop.create_task(self.send_msg(welcome_msg))
        logger.info(f"[{self.id}] initialized.")

    async def listen_for_msgs(self) -> None:
        while True:
            data = await self.event_loop.sock_recv(self.sock, 128)
            if len(data):
                try:
                    msg = data.decode("utf-8").strip()
                    self.on_msg(self.id, msg)

                except UnicodeDecodeError:
                    logger.error("Received a message which isn't in UTF8 format.")
                    self.sock.close()
                    break

    async def send_msg(self, msg: str) -> None:
        await self.event_loop.sock_sendall(self.sock, msg.encode("utf-8"))

        