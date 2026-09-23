import dask
from dask.array.core import from_imperative
import numpy as np
import inspect

def main():
    # Simulate imperative input
    value = dask.delayed(np.ones)(4)
    arr = from_imperative(value, shape=(4,), dtype=float)

    print("from_imperative result:", arr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(from_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()