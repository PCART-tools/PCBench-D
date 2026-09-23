import dask.dataframe as dd
from dask.dataframe import _Frame
import pandas as pd
import inspect

class MyFrame(_Frame):
    pass

def main():
    pdf = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    ddf = dd.from_pandas(pdf, npartitions=1)
    result = _Frame.to_imperative(ddf)
    print("to_imperative result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(_Frame.to_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()