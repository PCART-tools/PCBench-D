import numpy as np
import inspect
from io import StringIO

def main():
    data = StringIO("1,2,3\n4,5,6\n7,8,9")
    result = np.lib.npyio.mafromtxt(data, delimiter=",")
    print("mafromtxt result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.lib.npyio.mafromtxt))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()