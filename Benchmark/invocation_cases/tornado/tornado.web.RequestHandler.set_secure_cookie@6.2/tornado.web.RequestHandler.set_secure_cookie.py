import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.web
import tornado.httpclient
import inspect

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("my_cookie", "cookie_value", expires_days=1)
        print("Cookie set!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], cookie_secret="test-secret")

def main():
    app = make_app()
    server = app.listen(8888)  # bind to an available port
    print("Server running")

    io_loop = tornado.ioloop.IOLoop.current()
    async def trigger_request():
        try:
            client = tornado.httpclient.AsyncHTTPClient()
            resp = await client.fetch("http://localhost:8888/")
            print(resp.headers.get_list("Set-Cookie"))
        except Exception:
            raise 
        finally:
            server.stop() 
            io_loop.stop() 

    io_loop.add_callback(trigger_request)
    io_loop.start()
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.web.RequestHandler.set_secure_cookie))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
