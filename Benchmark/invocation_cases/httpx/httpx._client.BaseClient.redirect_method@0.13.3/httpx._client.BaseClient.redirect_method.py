import httpx
import inspect

from httpx._client import BaseClient
from httpx._models import Request, Response
from httpx import URL

def main():
    client = httpx.Client()

    request = Request(
        method="POST",
        url=URL("https://example.com/form"),
    )

    response = Response(
        status_code=302,
        headers={"Location": "https://example.com/get"},
        request=request,
    )

    new_method = BaseClient.redirect_method(
        client,
        request=request,
        response=response,
    )
    print("Redirect method:", new_method)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.redirect_method))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()