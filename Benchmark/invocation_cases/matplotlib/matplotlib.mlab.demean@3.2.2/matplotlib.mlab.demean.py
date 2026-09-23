import matplotlib.mlab as mlab
import inspect
import numpy as np

def main():
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = mlab.demean(data)
    print("demean result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mlab.demean))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()