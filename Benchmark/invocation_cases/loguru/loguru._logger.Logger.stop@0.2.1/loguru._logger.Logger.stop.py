from loguru import logger
import inspect

def main():
    result = logger.stop()
    print(result)
    print("Logger stopped.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(logger.stop))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
