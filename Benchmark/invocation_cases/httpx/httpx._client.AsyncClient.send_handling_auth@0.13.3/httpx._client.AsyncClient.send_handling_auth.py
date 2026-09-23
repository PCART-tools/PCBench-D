import asyncio
import inspect
import httpx

async def main():
    client = httpx.AsyncClient()
    request = httpx.Request("GET", "https://example.com")
    response = client.send_handling_auth(
        request,
        history=[],
        auth=client.auth,
        timeout=client.timeout,
    )

    print("Response:", response)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.send_handling_auth))
    except Exception as e:
        print(type(e).__name__)

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())