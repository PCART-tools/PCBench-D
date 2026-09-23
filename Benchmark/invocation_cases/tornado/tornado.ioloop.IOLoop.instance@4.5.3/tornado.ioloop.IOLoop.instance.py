import tornado.ioloop
import inspect

def main():
    ioloop_instance = tornado.ioloop.IOLoop.instance()
    print("IOLoop instance:", ioloop_instance)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.ioloop.IOLoop.instance))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()