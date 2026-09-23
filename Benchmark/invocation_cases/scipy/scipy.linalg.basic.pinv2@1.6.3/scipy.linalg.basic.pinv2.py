import numpy as np
from scipy.linalg import pinv2
import inspect

def main():
    matrix = np.array([[1, 2], [3, 4]])
    result = pinv2(matrix)
    print("pinv2 result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pinv2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()