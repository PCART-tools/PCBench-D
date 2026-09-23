import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    result = df.reindex_axis(['B', 'A'], axis=1)
    print("reindex_axis result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.reindex_axis))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()