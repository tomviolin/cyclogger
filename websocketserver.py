#!/usr/bin/env python3

import asyncio
from websockets.server import serve
import time
from threading import Thread


async def sendcycle(websocket):
    async for message in websocket:
        #print("sending ACK to client")
        #await websocket.send(f'{{"ACK":"message"}}')
        print("reading current data: ",end='',flush=True)
        thiscycledata = open("latest.json","r").read()
        print(thiscycledata)
        while True:
            print("sending data...")
            await websocket.send(thiscycledata)
            lastcycledata=thiscycledata
            print("waiting for new data...",end='',flush=True)
            while lastcycledata == thiscycledata:
                print(".",end='',flush=True)
                time.sleep(0)
                thiscycledata = open("latest.json","r").read()
            print("GOT IT!")

            


async def echo(websocket, dummy):
    # each message is a request for events to be sent
    await sendcycle(websocket)


async def main():
    async with serve(echo, "0.0.0.0", 6878):
        print("server loop")
        await asyncio.Future()  # run forever


print("** WEBSOCKET SERVER **")
asyncio.run(main())
