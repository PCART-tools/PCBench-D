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

    auth = httpx.Auth()
    timeout = Timeout(5.0)
    response = Client.send_handling_redirects(
        client,
        request,
        auth,
        timeout,
        True,      # allow_redirects
        None,      # history
    )

    print("Response:", response)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Client.send_handling_redirects))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()