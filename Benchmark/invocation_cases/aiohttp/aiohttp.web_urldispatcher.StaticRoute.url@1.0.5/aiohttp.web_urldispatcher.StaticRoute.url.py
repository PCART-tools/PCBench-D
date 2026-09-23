import aiohttp.web
import aiohttp.web_urldispatcher
import inspect
import os
import tempfile

def main():
    app = aiohttp.web.Application()

    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "example.txt")
    with open(test_file, "w") as f:
        f.write("test content")

    app.router.add_static('/static', tmpdir)

    static_route = None
    for route in app.router.routes():
        if isinstance(route, aiohttp.web_urldispatcher.StaticRoute):
            static_route = route
            break

    result = aiohttp.web_urldispatcher.StaticRoute.url(static_route,filename='example.txt')
    print("StaticRoute.url result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.web_urldispatcher.StaticRoute.url))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
