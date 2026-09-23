import numpy as np
import matplotlib.scale as mscale
import inspect

def main():
    transform = mscale.InvertedLog10Transform()
    data = np.array([1.0, 10.0, 100.0])
    result = transform.transform(data)

    print("InvertedLog10Transform result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.InvertedLog10Transform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()