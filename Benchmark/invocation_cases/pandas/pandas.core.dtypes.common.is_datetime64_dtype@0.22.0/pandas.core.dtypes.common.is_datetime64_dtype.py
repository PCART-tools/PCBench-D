import pandas as pd
import numpy as np
import inspect
from pandas.core.dtypes.common import is_datetime64_dtype

def main():
    arr = pd.Series(pd.date_range('20230101', periods=3))
    result = is_datetime64_dtype(arr)
    print("is_datetime64_dtype result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_datetime64_dtype))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()