import numpy as np
from scipy.integrate import quadrature
import inspect

def main():
    def func(x):
        return np.sin(x)

    result, error = quadrature(func, 0, np.pi)
    print("quadrature result:", result)
    print("quadrature error estimate:", error)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(quadrature))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()