import httpx
import inspect
from httpx._client import BaseClient
from httpx._models import Request
from httpx import URL, Headers

def main():
    client = httpx.Client()

    request = Request(
        method="POST",
        url="https://example.com/path",
        headers={
            "Authorization": "Bearer SECRET",
            "Content-Length": "123",
            "Cookie": "a=b",
            "User-Agent": "test-agent",
        },
    )

    redirect_url = URL("https://other.example.com/new")
    redirect_method = "GET"
    new_headers = BaseClient.redirect_headers(
        client,
        request=request,
        url=redirect_url,
        method=redirect_method,
    )

    print(dict(new_headers))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.redirect_headers))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()