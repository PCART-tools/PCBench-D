import numpy as np
from numpy.lib.function_base import unique
import inspect

def main():
    arr = np.array([1, 2, 2, 3, 4, 4, 5])
    result = unique(arr)
    print("unique result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(unique))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()