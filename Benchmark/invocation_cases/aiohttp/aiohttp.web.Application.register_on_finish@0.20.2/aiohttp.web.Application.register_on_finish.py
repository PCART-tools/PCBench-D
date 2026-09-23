import aiohttp.web
import inspect

def on_finish(app):
    print("Application is finishing.")

def main():
    app = aiohttp.web.Application()
    app.register_on_finish(on_finish)
    print("register_on_finish called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.web.Application.register_on_finish))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()