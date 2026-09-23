import httpx
import inspect

def main():
    query_params = httpx.QueryParams({"key": ["value1", "value2"], "other_key": "value3"})
    result = query_params.getlist("key")
    print("getlist result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx.QueryParams.getlist))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()