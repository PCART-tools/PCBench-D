import tornado.gen
import tornado.ioloop
import inspect

@tornado.gen.coroutine
def main():
    future1 = tornado.gen.sleep(0.1)
    future2 = tornado.gen.sleep(0.2)
    result = yield tornado.gen.multi_future([future1, future2])
    print("multi_future result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.gen.multi_future))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)