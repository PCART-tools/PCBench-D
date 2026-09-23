import pandas as pd
import inspect
from pandas.core.generic import NDFrame

def main():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    result = NDFrame.reindex_axis(df,['B', 'A'], axis=1)
    print("reindex_axis result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(NDFrame.reindex_axis))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()