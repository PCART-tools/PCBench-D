import tornado.web
import inspect


class FakeHandler(object):
    settings = {}
    locale = None
    request = None
    _reason = None

def main():
    fake = FakeHandler()
    html = tornado.web.RequestHandler.get_error_html(fake, 500)
    print("get_error_html result:", html)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.web.RequestHandler.get_error_html))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
