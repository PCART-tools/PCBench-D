import asyncio
from httpx._client import AsyncClient
from httpx._config import Proxy
from httpx import URL
import inspect

async def main():
    proxy = Proxy(
        url=URL("http://127.0.0.1:8888"),
        headers=None,
        mode="DEFAULT",
    )

    client = AsyncClient()
    transport = client.init_proxy_transport(proxy)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.init_proxy_transport))
    except Exception as e:
        print(type(e).__name__)

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())