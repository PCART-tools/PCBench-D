import tornado.ioloop
import tornado.web
import tornado.httpclient
import inspect

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.write("All cookies cleared.")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    app = make_app()
    server = app.listen(8888)  # bind to an available port
    print("Server running")

    io_loop = tornado.ioloop.IOLoop.current()
    async def trigger_request():
        try:
            client = tornado.httpclient.AsyncHTTPClient()
            resp = await client.fetch("http://localhost:8888/")
            print("Response:", resp.body.decode())
        except Exception:
            raise
        finally:
            server.stop() 
            io_loop.stop() 

    io_loop.add_callback(trigger_request)
    io_loop.start()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.web.RequestHandler.clear_all_cookies))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
