import asyncio
import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from sys import exit
from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()

class Client:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)

        loop.create_task(self.listen_for_messages())
        loop.create_task(self.send_user_input())

    async def listen_for_messages(self) -> None:
        while True:
            data = await loop.sock_recv(self.sock, 128)
            if len(data):
                try:
                    msg = data.decode("utf-8").strip()
                    logger.info(msg)
                except UnicodeDecodeError:
                    logger.error("Received a message which isn't in UTF8 format.")
                    self.disconnect()
                    break

    async def send_user_input(self) -> None:
        while True:
            msg = input()
            await loop.sock_sendall(self.sock, msg.encode("utf-8"))

    def disconnect(self) -> None:
        logger.info("Disconnecting.")
        exit(0)
        pass

host = input("Please enter server address: ")
port = int(input("Please enter server port: "))

client = Client(host, port)