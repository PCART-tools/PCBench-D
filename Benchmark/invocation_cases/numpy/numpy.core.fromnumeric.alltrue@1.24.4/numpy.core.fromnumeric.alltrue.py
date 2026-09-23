import numpy as np
import inspect

def main():
    arr = np.array([True, True, True, False])
    result = np.alltrue(arr)
    print("alltrue result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.alltrue))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()