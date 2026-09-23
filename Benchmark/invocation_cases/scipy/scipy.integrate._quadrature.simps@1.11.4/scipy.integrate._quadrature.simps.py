import numpy as np
from scipy.integrate import simps
import inspect

def main():
    y = np.array([1, 4, 9, 16])
    x = np.array([0, 1, 2, 3])
    result = simps(y, x)
    print("simps result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(simps))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()