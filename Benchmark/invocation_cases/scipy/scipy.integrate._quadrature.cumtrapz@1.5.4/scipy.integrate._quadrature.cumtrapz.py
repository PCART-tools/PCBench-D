import numpy as np
from scipy.integrate import cumtrapz
import inspect

def main():
    y = np.array([0, 1, 2, 3, 4])
    x = np.array([0, 1, 2, 3, 4])
    result = cumtrapz(y, x)
    print("cumtrapz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cumtrapz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()