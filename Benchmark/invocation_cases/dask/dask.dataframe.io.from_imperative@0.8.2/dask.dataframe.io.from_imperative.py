import dask.dataframe as dd
import pandas as pd
import dask
import inspect

def main():
    # Simulate an imperative dask computation
    data = dask.delayed(lambda: [1, 2, 3, 4])()
    meta = pd.DataFrame(columns=['a', 'b', 'c'])
    df = dd.io.from_imperative(data,meta)
    print("from_imperative result:")
    print(df.compute())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dd.io.from_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()