import asyncio
import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from typing import List
from socket import socket, AF_INET, SOCK_STREAM
from connection import Connection

logger = logging.getLogger(__name__)

PORT = 5000

loop = asyncio.get_event_loop()

class Server:
    sock: socket = socket(AF_INET, SOCK_STREAM)
    connections: List[Connection] = []

    def __init__(self) -> None:
        self.sock.setblocking(False)

    def start(self, port: int):
        logger.info(f"Starting the server on port: {port}")

        self.sock.bind(("localhost", port))
        self.sock.listen(8)

    async def accept_connections(self) -> None:
        logger.info("Listening for new connections.")
        while True:
            conn, address = await loop.sock_accept(self.sock)
            logger.info(f"Received a new connection from: {address}")
            connection = Connection(loop, conn, address, self.broadcast_msg, self.remove_connection)

            self.connections.append(connection)

    def broadcast_msg(self, from_con_id: str, msg: str) -> None:
        logger.info(f"[{from_con_id}]: {msg}")

        counter = 0
        for conn in filter(lambda c: c.id != from_con_id, self.connections):
            loop.create_task(conn.send_msg(f"[{from_con_id}]: {msg}\n"))
            counter += 1

        logger.info(f"Broadcasted to {counter} clients.")

    def remove_connection(self, con_id) -> None:
        self.connections = list(filter(lambda c: c.id != con_id, self.connections))

    def stop(self) -> None:
        logger.info("Stopping the server.")
        self.sock.close()

server = Server()
server.start(PORT)
loop.run_until_complete(server.accept_connections())