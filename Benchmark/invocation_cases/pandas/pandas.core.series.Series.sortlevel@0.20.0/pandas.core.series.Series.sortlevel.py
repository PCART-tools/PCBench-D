import pandas as pd
import inspect

def main():
    data = pd.Series([1, 2, 3], index=pd.MultiIndex.from_tuples([('a', 1), ('a', 2), ('b', 1)]))
    result = data.sortlevel(level=0)
    print("sortlevel result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.sortlevel))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()