import httpx
import inspect
from httpx._client import BaseClient

def main():
    # Create httpx.Client instance and merge headers
    client = httpx.Client(headers={"User-Agent": "test-agent"})
    additional_headers = {"Authorization": "Bearer test-token"}
    result = BaseClient.merge_headers(client, additional_headers)
    print("merge_headers result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.merge_headers))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
