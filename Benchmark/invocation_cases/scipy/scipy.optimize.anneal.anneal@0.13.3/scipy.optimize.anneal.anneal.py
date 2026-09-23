import numpy as np
from scipy.optimize import anneal
import inspect

def main():
    def func(x):
        return np.sin(x) + np.cos(x)

    result = anneal(func, x0=0.0)
    print("anneal result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(anneal))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()