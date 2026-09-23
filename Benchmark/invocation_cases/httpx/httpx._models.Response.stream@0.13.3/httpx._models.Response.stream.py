import httpx
import inspect
import asyncio
from httpx._models import Response,Request

async def main():
    request = Request("GET", "https://example.com")

    response = Response(
        status_code=200,
        request=request,
        content=b"hello\nworld\n"
    )

    agen = response.stream()
    print(agen)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(response.stream))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.run(main())