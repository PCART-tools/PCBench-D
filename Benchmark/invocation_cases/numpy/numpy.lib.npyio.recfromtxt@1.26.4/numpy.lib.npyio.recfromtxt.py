import numpy as np
import inspect
from io import StringIO

def main():
    data = StringIO("1,2,3\n4,5,6")
    result = np.recfromtxt(data, delimiter=",", names=True, dtype=None, encoding=None)
    print("recfromtxt result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.recfromtxt))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()