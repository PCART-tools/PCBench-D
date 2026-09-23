import tornado.httpserver
import inspect

class DummyStream:
    def set_close_callback(self, cb):
        pass

class DummyContext:
    remote_ip = "127.0.0.1"

class DummyConnection:
    context = DummyContext()
    xheaders = False
    stream = DummyStream()

def main():
    request = tornado.httpserver.HTTPRequest(method="GET", uri="/",connection=DummyConnection())
    print("HTTPRequest method:", request.method)
    print("HTTPRequest uri:", request.uri)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.httpserver.HTTPRequest))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()