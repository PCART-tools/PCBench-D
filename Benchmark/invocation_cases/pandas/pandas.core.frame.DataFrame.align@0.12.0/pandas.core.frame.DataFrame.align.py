import pandas as pd
import inspect

def main():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    aligned_df1, aligned_df2 = df1.align(df2)
    print("Aligned DataFrame 1:\n", aligned_df1)
    print("Aligned DataFrame 2:\n", aligned_df2)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.align))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()