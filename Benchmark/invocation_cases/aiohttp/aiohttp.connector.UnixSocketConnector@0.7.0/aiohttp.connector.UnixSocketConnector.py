import aiohttp
import asyncio
import inspect

async def main():
    connector = aiohttp.UnixSocketConnector(path='/tmp/socket')
    print("UnixSocketConnector created:", connector)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.UnixSocketConnector))
    except Exception as e:
        print(type(e).__name__)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())