import pandas as pd
import inspect

def main():
    df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'value': [1, 2, 3]})
    df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'value': [4, 5, 6]})
    result = pd.tools.merge.ordered_merge(df1, df2, on='key')
    print("ordered_merge result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.tools.merge.ordered_merge))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()