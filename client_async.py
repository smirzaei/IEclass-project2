import asyncio
import logging
LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(logging.INFO)

from sys import exit
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from functools import partial

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def connect(self) -> None:
        logger.info(f"Connecting to {self.host}:{self.port}")
        reader, writer = await asyncio.open_connection(self.host, self.port)

        self.reader = reader
        self.writer = writer

    async def send(self, msg: str) -> None:
        self.writer.write(msg.encode("utf-8"))
        await self.writer.drain()

    async def listen_for_messages(self) -> None:
        logger.info("Listening for server messages.")

        while True:
            data = await self.reader.read(256)
            if len(data):
                try:
                    msg = data.decode("utf-8").strip()
                    logger.info(msg)
                except UnicodeDecodeError:
                    logger.error("Received a message which isn't in UTF8 format.")
                    await self.disconnect()
                    break
            else:
                logger.warn("Socket disconnected.")
                await self.disconnect()
                break

    async def send_user_input(self) -> None:
        logger.info("Listening for user input.")

        while True:
            logger.info("waiting for user input")
            msg = input()
            logger.info("got input")
            await self.send(msg)
            logger.info("sent input")

    async def disconnect(self) -> None:
        logger.info("Disconnecting.")
        
        self.writer.close()
        await self.writer.wait_closed()
        
        exit(0)

    async def test(self) -> None:
        counter = 0
        while True:
            counter += 1
            logger.info(counter)
            await asyncio.sleep(1)

async def run():
    host = input("Please enter server address: ")
    port = int(input("Please enter server port: "))

    client = Client(host, port)
    await client.connect()

    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(ThreadPoolExecutor(1), client.send_user_input)
    
    # input_thread = Thread(target=client.send_user_input, args=())
    # input_thread.start()

    t = asyncio.create_task(client.test())
    # t2 = asyncio.create_task(client.listen_for_messages())
    await t
    # await t2
    

    # dummy_task = asyncio.create_task(client.test())
    # await dummy_task

    # await client.listen_for_messages()
    #read_task = asyncio.create_task(client.listen_for_messages())
    #send_msg_task = asyncio.create_task(client.send_user_input())
    
    # await client.send_user_input()

#     await asyncio.wait([
#         read_task,
#  #       send_msg_task
#     ])

    await client.disconnect()
    
asyncio.run(run())