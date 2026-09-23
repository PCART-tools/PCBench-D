from loguru import logger
import inspect

def main():
    # Simulate starting a logger with a file sink
    logger.start("file.log")
    print("Logger started with file sink.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(logger.start))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()