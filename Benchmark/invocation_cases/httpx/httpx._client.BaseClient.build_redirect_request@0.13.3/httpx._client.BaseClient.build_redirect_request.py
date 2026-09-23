import httpx
from httpx import Request, Response
import inspect

def main():
    client = httpx.Client()
    request = Request(
        method="GET",
        url="https://example.com/old",
    )

    response = Response(
        status_code=302,
        headers={
            "Location": "/new"
        },
        request=request,  
    )

    next_request = httpx._client.BaseClient.build_redirect_request(
        client,
        request,
        response,
    )
    print( next_request)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx._client.BaseClient.build_redirect_request))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
