import numpy as np
import inspect

def main():
    arr = np.array([1.234, 5.678, 9.1011])
    formatter = np.core.arrayprint.FloatFormat(data=arr, precision=2, suppress_small=True)
    formatted = [formatter(x) for x in arr]
    print("Formatted result:", formatted)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.arrayprint.FloatFormat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()