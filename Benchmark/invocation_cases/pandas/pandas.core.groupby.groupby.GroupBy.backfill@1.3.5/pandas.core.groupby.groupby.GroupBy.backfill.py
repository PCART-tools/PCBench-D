import pandas as pd
import inspect
from pandas.core.groupby import GroupBy

def main():
    data = {'A': [1, None, 3, None, 5], 'B': [None, 2, None, 4, None]}
    df = pd.DataFrame(data)
    grouped = df.groupby(df.index // 2)
    result = GroupBy.backfill(grouped)
    print("backfill result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GroupBy.backfill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()