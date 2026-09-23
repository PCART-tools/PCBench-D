import aiohttp.web
import inspect

def main():
    app = aiohttp.web.Application()
    result = app.finish()
    print("finish result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.web.Application.finish))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()