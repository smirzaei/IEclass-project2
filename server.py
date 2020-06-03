import asyncio
import logging
LOG_FORMAT = "%(asctime)s - %(funcName)s:%(lineno)s [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from typing import Tuple, List, Any
from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)

PORT = 5000

loop = asyncio.get_event_loop()

class Server:
    sock: socket = socket(AF_INET, SOCK_STREAM)
    connections: List[Tuple[socket, Any]] = []

    def __init__(self) -> None:
        self.sock.setblocking(False)

    def start(self, port: int):
        logger.info(f"Starting the server on port: {port}")
        
        self.sock.bind(("localhost", port))
        self.sock.listen(8)

    async def accept_connections(self):
        logger.info("Listening for new connections.")
        while True:
            connection, address = await loop.sock_accept(self.sock)
            logger.info(f"Received a new connection from: {address}")

            self.connections.append((connection, address))


    def stop(self):
        logger.info("Stopping the server.")
        self.sock.close()

server = Server()
server.start(PORT)
loop.run_until_complete(server.accept_connections())