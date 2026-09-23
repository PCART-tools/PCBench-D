import httpx
import inspect

def main():
    # Simulate a client to access the internal method
    client = httpx.Client()

    if hasattr(client, "_proxies"):
        proxies = client._proxies
    else:
        proxies = client.proxies         
    trust_env = client.trust_env 

    proxy_map = httpx._client.BaseClient.get_proxy_map(
        client,
        proxies,
        trust_env,
    )
    print("get_proxy_map result:", proxy_map)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx._client.BaseClient.get_proxy_map))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()