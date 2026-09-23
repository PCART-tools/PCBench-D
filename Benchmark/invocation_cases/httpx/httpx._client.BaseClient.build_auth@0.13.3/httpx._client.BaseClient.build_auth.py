import httpx
import inspect

def main():
    client = httpx.Client()
    request = httpx.Request("GET", "http://example.com")
    auth = httpx._client.BaseClient.build_auth(client, request)
    print("build_auth result:", auth)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx._client.BaseClient.build_auth))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()