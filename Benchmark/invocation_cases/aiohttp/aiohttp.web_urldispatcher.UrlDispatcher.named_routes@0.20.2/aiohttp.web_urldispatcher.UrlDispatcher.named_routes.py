import aiohttp.web_urldispatcher as web_urldispatcher
import inspect

def main():
    dispatcher = web_urldispatcher.UrlDispatcher()
    named_routes = dispatcher.named_routes()
    print("named_routes result:", named_routes)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(web_urldispatcher.UrlDispatcher.named_routes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()