import httpx
import inspect

from httpx._client import BaseClient
from httpx._models import Request, Response
from httpx import URL, Headers

def main():
    client = httpx.Client()

    request = Request(
        method="GET",
        url="http://example.com/old",
    )

    response = Response(
        status_code=302,
        headers=Headers(
            {
                "Location": "/new/path"
            }
        ),
        request=request,
    )

    new_url = BaseClient.redirect_url(
        client,
        request=request,
        response=response,
    )
    print("redirect_url:", new_url)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.redirect_url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()