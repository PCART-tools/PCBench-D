import httpx
import inspect
from httpx._client import BaseClient

def main():
    base_url = "https://example.com"
    relative_url = "/path"

    client = httpx.Client(base_url=base_url)

    merged_url = BaseClient.merge_url(client, relative_url)
    print("Merged URL:", merged_url)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.merge_url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()