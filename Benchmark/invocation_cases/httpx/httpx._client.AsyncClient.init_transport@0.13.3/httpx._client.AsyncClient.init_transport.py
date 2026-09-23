import asyncio
import inspect
from httpx._client import AsyncClient

async def main():
    client = AsyncClient()

    transport = client.init_transport()
    print("Transport:", transport)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.init_transport))
    except Exception as e:
        print(type(e).__name__)

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())