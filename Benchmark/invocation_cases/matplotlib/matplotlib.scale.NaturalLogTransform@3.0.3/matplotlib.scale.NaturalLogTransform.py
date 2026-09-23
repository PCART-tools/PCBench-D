import matplotlib.scale as mscale
import numpy as np
import inspect

def main():
    transform = mscale.NaturalLogTransform()
    data = np.array([1.0, np.e, np.e**2, np.e**3])
    result = transform.transform(data)
    print("NaturalLogTransform result:", result)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mscale.NaturalLogTransform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()