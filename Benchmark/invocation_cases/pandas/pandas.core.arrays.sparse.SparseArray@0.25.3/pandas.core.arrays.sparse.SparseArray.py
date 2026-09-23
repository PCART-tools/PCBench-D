import pandas as pd
import inspect
from pandas.core.arrays.sparse import SparseArray

def main():
    data = [0, 0, 1, 0, 2]
    sparse_array = SparseArray(data)
    print("SparseArray:", sparse_array)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SparseArray))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()