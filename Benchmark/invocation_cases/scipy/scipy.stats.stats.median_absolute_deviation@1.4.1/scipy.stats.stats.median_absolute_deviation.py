import scipy.stats as stats
import inspect
import numpy as np

def main():
    data = np.array([1, 2, 3, 4, 5, 6, 7])
    result = stats.median_absolute_deviation(data)
    print("median_absolute_deviation result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(stats.median_absolute_deviation))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()