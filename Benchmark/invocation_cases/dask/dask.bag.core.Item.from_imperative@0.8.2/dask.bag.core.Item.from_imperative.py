import dask.bag as db
from dask.bag.core import Item
import inspect
from dask import do

def read_file(fn):
    with open(fn, "r") as f:
        return f.read().strip()

def main():
    filenames = ['./file1.txt', './file2.txt']

    for i, fn in enumerate(filenames, 1):
        with open(fn, 'w') as f:
            f.write(f'hello from file{i}\n')

    values = [do(read_file)(fn) for fn in filenames]
    items = [Item.from_imperative(v) for v in values]
    result = [it.compute() for it in items]
    print("from_filenames result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Item.from_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
