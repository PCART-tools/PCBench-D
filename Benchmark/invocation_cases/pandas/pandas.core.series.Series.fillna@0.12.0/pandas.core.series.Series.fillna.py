import pandas as pd
import inspect

def main():
    # Create a Series with missing values
    s = pd.Series([1, 2, None, 4, None, 6])
    # Fill missing values with 0
    result = s.fillna(0)
    print("fillna result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.fillna))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()