import dask
from dask.imperative import value
import inspect

def main():
    # Simulate a computation
    x = value(42)
    result = x.compute()
    print("value compute result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(value))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()