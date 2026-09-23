import httpx
import inspect

def main():
    client = httpx.Client()
    request = httpx.Request("GET", "https://httpbin.org/get")
    history = []
    auth = httpx.Auth()
    timeout = client.timeout
    response = client.send_handling_auth(
        request=request,
        history=history,
        auth=auth,
        timeout=timeout,
    )
    print("send_handling_auth result:", response)
    
    print("-----getsource_output-----")
    try:
        # Get the source code of the target API
        print(inspect.getsource(client.send_handling_auth))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()