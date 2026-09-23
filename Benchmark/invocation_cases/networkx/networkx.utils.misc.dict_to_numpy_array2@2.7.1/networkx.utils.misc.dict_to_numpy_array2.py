from networkx.utils.misc import dict_to_numpy_array2
import numpy as np
import inspect

def main():
    d = {
        0: {0: 1},
        1: {1: 2},
        2: {2: 3},
    }

    result = dict_to_numpy_array2(d)

    print("dict_to_numpy_array2 result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dict_to_numpy_array2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()