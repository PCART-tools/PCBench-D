import numpy as np
import inspect

def main():
    arr = np.array([1.234, 2.345, 3.456])
    result = np.round_(arr, decimals=1)
    print("round_ result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.round_))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()