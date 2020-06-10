import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from sys import exit
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.sock = socket(AF_INET, SOCK_STREAM)
        
    def connect(self) -> None:
        logger.info(f"Connecting to {self.host}:{self.port}")
        self.sock.connect((self.host, self.port))

    def receve_msg(self) -> None:
        while True:
            try:
                data = self.sock.recv(256)
                if len(data) > 0:
                    print(data.decode(encoding='utf-8').strip())
                else:
                    logger.info("Connection closed.")
                    self.disconnect()
                    break
            except:
                logger.info("An error occurred.")
                self.disconnect()
                break

    def listen_and_send_user_input(self) -> None:
        logger.info("Listening for user input.")

        while True:
            inpt = input()
            self.sock.sendall(inpt.encode("utf-8"))


    def disconnect(self) -> None:
        logger.info("Disconnecting.")
        self.sock.close()
        exit(0)

host = input("Please enter server address: ")
port = int(input("Please enter server port: "))

client = Client(host, port)
client.connect()

thread = Thread(target=client.listen_and_send_user_input)
thread.start()

client.receve_msg()








