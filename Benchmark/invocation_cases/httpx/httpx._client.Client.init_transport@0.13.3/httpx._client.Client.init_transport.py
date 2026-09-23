import httpx
import inspect
from httpx._client import Client

def main():
    client = Client()
    Client.init_transport(client, None)
    print("Transport initialized.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Client.init_transport))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()