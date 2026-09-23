import tornado.netutil
import inspect

def main():
    server = tornado.netutil.TCPServer()
    print("TCPServer instance created:", server)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.netutil.TCPServer))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()