import httpx
import inspect

def main():
    client = httpx.Client()

    cookies = {"session_id": "abc123"}
    merged = httpx._client.BaseClient.merge_cookies(
        client,
        cookies,
    )

    print("Merged cookies:", merged)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx._client.BaseClient.merge_cookies))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
