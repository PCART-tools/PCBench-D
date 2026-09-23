import numpy as np
from scipy.integrate import romberg
import inspect

def main():
    # Define a simple function to integrate
    def f(x):
        return x**2

    # Use romberg integration on the function f from 0 to 1
    result = romberg(f, 0, 1)
    print("romberg result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(romberg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()