import polars as pl
import inspect

def main():
    # Call the target API
    size = pl.threadpool_size()
    print("threadpool_size result:", size)

    # Get the source code of the target API
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.threadpool_size))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()