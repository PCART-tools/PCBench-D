import pandas as pd
from pandas import Series
import inspect

def main():
    data = pd.Series([1, 2, 3, 4, 5],dtype=float)
    cond = data > 3
    result = Series.mask(data,cond)
    print("mask result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Series.mask))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()