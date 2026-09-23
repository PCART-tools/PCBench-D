import pandas as pd
import inspect
from pandas.core.dtypes.common import is_categorical

def main():
    series = pd.Series(pd.Categorical(['a', 'b', 'c']))
    result = is_categorical(series)
    print("is_categorical result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_categorical))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()