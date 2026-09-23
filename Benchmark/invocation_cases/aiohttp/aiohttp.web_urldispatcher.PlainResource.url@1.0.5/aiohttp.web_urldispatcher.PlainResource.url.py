import aiohttp.web
import inspect

def main():
    app = aiohttp.web.Application()

    async def handler(request):
        return aiohttp.web.Response(text="ok")

    route = app.router.add_route('GET', '/test', handler)
    resource = route.resource
    url = resource.url()
    print("PlainResource.url result:", str(url))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(resource.url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
