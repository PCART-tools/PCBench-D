import numpy as np
import inspect

def main():
    arr = np.array(['hello', 'world'])
    char_arr = np.core.defchararray.chararray(arr.shape, itemsize=10)
    char_arr[:] = arr
    print("chararray result:", char_arr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.defchararray.chararray))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()