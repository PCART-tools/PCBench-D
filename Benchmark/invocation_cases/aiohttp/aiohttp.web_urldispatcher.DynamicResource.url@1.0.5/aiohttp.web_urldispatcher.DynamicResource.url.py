import aiohttp
import inspect
from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, world")

async def main():
    app = web.Application()
    resource = app.router.add_resource('/{name}')
    #dynamic_resource = resource.add_route('GET', handle)

    url = resource.url(parts={'name': 'test'})
    print("DynamicResource.url result:", url)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(resource.url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())