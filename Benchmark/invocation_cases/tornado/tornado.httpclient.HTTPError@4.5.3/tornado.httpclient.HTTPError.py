import tornado.httpclient
import inspect

def main():
    try:
        raise tornado.httpclient.HTTPError(404, "Not Found")
    except tornado.httpclient.HTTPError as e:
        print("HTTPError:", e)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.httpclient.HTTPError))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()