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
        self.sock.setblocking(False)

    async def connect(self) -> None:
        logger.info(f"Connecting to {self.host}:{self.port}")
        await loop.sock_connect(self.sock, (self.host, self.port))

    async def listen_for_messages(self) -> None:
        logger.info("Listening for server messages.")

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
        logger.info("Listening for user input.")

        while True:
            msg = input()
            await loop.sock_sendall(self.sock, msg.encode("utf-8"))


    def disconnect(self) -> None:
        logger.info("Disconnecting.")
        exit(0)
        pass

async def run():
    host = input("Please enter server address: ")
    port = int(input("Please enter server port: "))

    client = Client(host, port)
    await client.connect()

    send_user_input_task = loop.create_task(client.send_user_input())
    listen_for_msg_task = loop.create_task(client.listen_for_messages())
    
    await asyncio.wait([
        listen_for_msg_task,
        send_user_input_task
    ])
    exit(0)



loop.run_until_complete(run())