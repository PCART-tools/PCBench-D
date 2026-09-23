import numpy as np
import inspect

def main():
    sample = np.random.rand(100, 3)
    bins = [5, 5, 5]
    result, edges = np.histogramdd(sample, bins=bins)
    print("histogramdd result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.histogramdd))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()