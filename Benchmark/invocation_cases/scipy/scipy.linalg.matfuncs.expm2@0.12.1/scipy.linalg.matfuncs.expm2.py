import scipy.linalg
import inspect
import numpy as np

def main():
    matrix = np.array([[0, 1], [-1, 0]])
    result = scipy.linalg.matfuncs.expm2(matrix)
    print("expm2 result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(scipy.linalg.matfuncs.expm2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()