import aiohttp
import inspect

def main():
    jar = aiohttp.helpers.DummyCookieJar()
    print("DummyCookieJar created:", jar)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.helpers.DummyCookieJar))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()