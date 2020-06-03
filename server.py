import logging
LOG_FORMAT = "%(asctime)s - %(funcName)s:%(lineno)s [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)

PORT = 5000

class Server:
    sock = socket(AF_INET, SOCK_STREAM)

    def start(self, port: int):
        logger.info(f"Starting the server on port: {port}")
        
        self.sock.bind(("localhost", port))
        self.sock.listen(1)

    def stop(self):
        logger.info("Stopping the server.")
        self.sock.close()

server = Server()
server.start(PORT)