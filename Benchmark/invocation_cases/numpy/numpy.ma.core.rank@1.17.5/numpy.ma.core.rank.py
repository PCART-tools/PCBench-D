import numpy as np
import inspect

def main():
    arr = np.ma.array([[1, 2, 3], [4, 5, 6]])
    result = np.ma.rank(arr)
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.ma.rank))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()