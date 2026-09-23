import aiohttp
import inspect

def main():
    # Simulate a WebSocket message
    message = aiohttp.websocket.Message(aiohttp.websocket.MSG_TEXT, b"Hello, WebSocket!", 1)
    print("Message data:", message.data)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.websocket.Message))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()