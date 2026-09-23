import pandas as pd
import inspect

def main():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=[0, 1])
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]}, index=[0, 1])
    result = df1._indexed_same(df2)
    print("_indexed_same result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame._indexed_same))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()