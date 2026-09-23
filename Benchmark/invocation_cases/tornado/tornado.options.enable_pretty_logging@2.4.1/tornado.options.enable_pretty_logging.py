import tornado.options
import inspect

def main():
    tornado.options.enable_pretty_logging()
    print("enable_pretty_logging called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tornado.options.enable_pretty_logging))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()