import pandas as pd
import numpy as np
import inspect
from pandas.core.arrays.numpy_ import PandasArray

def main():
    data = np.array([1, 2, 3, 4, 5])
    pandas_array = PandasArray(data)
    print("PandasArray result:", pandas_array)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PandasArray))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()