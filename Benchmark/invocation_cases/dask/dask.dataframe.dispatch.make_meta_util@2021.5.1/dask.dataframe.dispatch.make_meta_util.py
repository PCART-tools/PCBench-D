import pandas as pd
import dask.dataframe as dd
import inspect

def main():
    # Create a sample DataFrame
    df = dd.from_pandas(
        pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), 
        npartitions=2
    )
    
    # Call the target API
    result = dd.dispatch.make_meta_util(df)
    print("make_meta_util result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dd.dispatch.make_meta_util))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()