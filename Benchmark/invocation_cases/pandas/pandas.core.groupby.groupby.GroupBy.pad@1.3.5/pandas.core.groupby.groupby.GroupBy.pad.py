import pandas as pd
import inspect
from pandas.core.groupby import GroupBy

def main():
    data = {'A': [1, 2, None, 4, None, 6], 'B': [None, 2, 3, None, 5, 6]}
    df = pd.DataFrame(data)
    grouped = df.groupby(df['A'].notna().cumsum())
    result = GroupBy.pad(grouped)
    print("pad result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GroupBy.pad))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()