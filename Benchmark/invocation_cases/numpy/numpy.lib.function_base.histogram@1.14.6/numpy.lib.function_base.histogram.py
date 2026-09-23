import numpy as np
import inspect

def main():
    data = np.array([1, 2, 1, 2, 3, 4, 5, 1])
    hist, bin_edges = np.histogram(data, bins=3)
    print("Histogram result:", hist)
    print("Bin edges:", bin_edges)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.histogram))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()