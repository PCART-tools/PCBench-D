import numpy as np
import inspect

def main():
    arr = np.array([1, 2, 3, 4])
    result = np.product(arr)
    print("product result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.product))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()