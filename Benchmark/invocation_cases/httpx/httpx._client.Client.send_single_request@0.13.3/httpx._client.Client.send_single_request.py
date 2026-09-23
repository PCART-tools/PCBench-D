import httpx
import inspect

from httpx._client import Client
from httpx._models import Request
from httpx import Timeout


def main():
    client = Client()
    request = Request(
        method="GET",
        url="https://httpbin.org/get",
    )

    timeout = Timeout(5.0)
    response = Client.send_single_request(
        client,
        request,
        timeout,
    )

    print("Response:", response)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Client.send_single_request))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()