import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    pd.DataFrame.__setattr__(df, "new_column", [5, 6])
    print("DataFrame with new column:\n", df)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__setattr__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()