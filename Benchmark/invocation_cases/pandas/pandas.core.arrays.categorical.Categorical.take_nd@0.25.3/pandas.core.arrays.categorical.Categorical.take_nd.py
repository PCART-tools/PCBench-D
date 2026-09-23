import pandas as pd
import numpy as np
import inspect
from pandas.core.arrays.categorical import Categorical

def main():
    categories = ['a', 'b', 'c']
    codes = [0, 1, 2, 0, 1]
    cat = Categorical.from_codes(codes, categories)
    indices = [0, 2, 4]
    result = cat.take_nd(indices)
    print("take_nd result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Categorical.take_nd))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()