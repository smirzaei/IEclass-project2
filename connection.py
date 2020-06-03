import logging

from asyncio.events import AbstractEventLoop
from typing import Callable, Any
from socket import socket

logger = logging.getLogger(__name__)

class Connection:
    def __init__(
        self,
        event_loop: AbstractEventLoop,
        sock: socket,
        address: Any,
        on_msg: Callable[[Any, str], None]
    ) -> None:
        self.sock = sock
        self.event_loop = event_loop
        self.address = address
        self.on_msg = on_msg

        event_loop.create_task(self.listen_for_msgs())

    async def listen_for_msgs(self) -> None:
        while True:
            data = await self.event_loop.sock_recv(self.sock, 128)
            if len(data):
                try:
                    msg = data.decode("utf-8").strip()
                    self.on_msg(self, msg)

                except UnicodeDecodeError:
                    logger.error("Received a message which isn't in UTF8 format.")
                    self.sock.close()
                    break



        