import asyncio
import inspect
import httpx

async def main():
    client = httpx.AsyncClient()

    request = httpx.Request("GET", "https://httpbin.org/get")

    response = client.send_handling_redirects(
        request=request,
        auth=client.auth,
        timeout=client.timeout,
        allow_redirects=True,
    )
    print("send_handling_redirects result:", response)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.send_handling_redirects))
    except Exception as e:
        print(type(e).__name__)

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())