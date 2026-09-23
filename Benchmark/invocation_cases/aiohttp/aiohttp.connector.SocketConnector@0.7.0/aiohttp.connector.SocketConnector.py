import aiohttp
import asyncio
import inspect

async def main():
    connector = aiohttp.connector.SocketConnector()
    print("BaseConnector created:", connector)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.connector.SocketConnector))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())