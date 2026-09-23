import tornado.platform.twisted
import inspect

def main():
    resolver = tornado.platform.twisted.TwistedResolver()
    print("TwistedResolver instance:", resolver)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.platform.twisted.TwistedResolver))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()