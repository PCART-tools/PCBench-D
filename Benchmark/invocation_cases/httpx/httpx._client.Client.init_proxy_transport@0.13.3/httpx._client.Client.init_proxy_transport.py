import httpx
import inspect
from httpx import Proxy

def main():
    client = httpx.Client()
    
    proxy = Proxy("http://example.com")

    transport = client.init_proxy_transport(
        proxy=proxy,
        verify=True,
        http2=False,
    )
    print("init_proxy_transport result:", transport)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(client.init_proxy_transport))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()