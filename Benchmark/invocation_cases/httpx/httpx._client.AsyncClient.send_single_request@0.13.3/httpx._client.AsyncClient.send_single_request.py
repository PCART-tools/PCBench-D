import asyncio
import inspect
import httpx

async def main():
    client = httpx.AsyncClient()
    request = httpx.Request("GET", "https://httpbin.org/get")
    response = client.send_single_request(
        request=request,
        timeout=client.timeout,
    )
    print("send_single_request result:", response)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.send_single_request))
    except Exception as e:
        print(type(e).__name__)

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())