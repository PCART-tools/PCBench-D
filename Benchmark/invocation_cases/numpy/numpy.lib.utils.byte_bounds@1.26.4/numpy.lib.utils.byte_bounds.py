import numpy as np
import inspect

def main():
    arr = np.array([1, 2, 3, 4, 5])
    result = np.byte_bounds(arr)
    print("byte_bounds result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.byte_bounds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()