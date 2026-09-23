import numpy as np
import inspect

def main():
    arr = np.array([False, False, True, False])
    result = np.sometrue(arr)
    print("sometrue result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.sometrue))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()