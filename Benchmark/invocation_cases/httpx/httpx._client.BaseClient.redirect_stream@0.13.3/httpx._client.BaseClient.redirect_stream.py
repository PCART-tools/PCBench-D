import httpx
import inspect

from httpx._client import BaseClient
from httpx._models import Request

class DummyStream:
    def __iter__(self):
        yield b"test"

    def close(self):
        pass


def main():
    client = httpx.Client()

    request = Request(
        method="POST",
        url="https://example.com/upload",
    )

    stream = DummyStream()

    new_stream = BaseClient.redirect_stream(
        client,
        request=request,
        method="GET",           
    )

    print("new_stream:", new_stream)   

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.redirect_stream))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()