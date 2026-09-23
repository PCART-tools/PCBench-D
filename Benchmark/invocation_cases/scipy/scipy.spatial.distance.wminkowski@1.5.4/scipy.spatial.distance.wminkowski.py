import numpy as np
from scipy.spatial.distance import wminkowski
import inspect

def main():
    # Test data
    u = np.array([1, 2, 3])
    v = np.array([4, 5, 6])
    p = 2
    w = np.array([0.5, 1.0, 1.5])
    
    # Call the wminkowski function
    result = wminkowski(u, v, p, w)
    print("wminkowski result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(wminkowski))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()