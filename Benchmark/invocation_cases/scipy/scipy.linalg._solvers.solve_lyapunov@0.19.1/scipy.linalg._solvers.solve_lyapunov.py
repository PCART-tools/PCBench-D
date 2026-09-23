import scipy.linalg
import inspect
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    q = np.array([[5, 6], [7, 8]])
    result = scipy.linalg.solve_lyapunov(a, q)
    print("solve_lyapunov result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(scipy.linalg.solve_lyapunov))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()