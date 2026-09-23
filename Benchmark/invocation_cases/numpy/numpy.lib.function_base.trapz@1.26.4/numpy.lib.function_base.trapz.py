import numpy as np
import inspect

def main():
    y = np.array([1, 2, 3, 4])
    x = np.array([0, 1, 2, 3])
    result = np.trapz(y, x)
    print("trapz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.trapz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()