from dask.bag.core import from_imperative
from dask.imperative import do
import inspect

def main():
    data = [1, 2, 3, 4, 5]
    values = [do(lambda x: x)(i) for i in data]
    items = [from_imperative(v) for v in values]
    result = [it.compute() for it in items]
    print("from_filenames result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(from_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()