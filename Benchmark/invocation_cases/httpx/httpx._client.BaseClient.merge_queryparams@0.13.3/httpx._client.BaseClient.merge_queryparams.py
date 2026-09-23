import httpx
import inspect
from httpx._client import BaseClient

def main():
    base_url = "https://example.com/api"
    params = {"key1": "value1", "key2": "value2"}

    client = httpx.Client()
    merged_query = BaseClient.merge_queryparams(client,params)
    print("merge_query_params result:", merged_query)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseClient.merge_queryparams))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
