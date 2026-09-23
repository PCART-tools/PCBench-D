import aiohttp
from aiohttp import web
import inspect

async def handle(request):
    return web.Response(text="Hello, world")

def main():
    app = web.Application()
    route = app.router.add_get('/', handle)
    url = route.url()
    print("Route URL:", url)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(route.url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()