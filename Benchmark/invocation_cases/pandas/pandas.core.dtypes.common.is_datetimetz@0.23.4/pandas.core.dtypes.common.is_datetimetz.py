import pandas as pd
import numpy as np
import inspect
from pandas.core.dtypes.common import is_datetimetz

def main():
    # Create a datetime index with timezone
    dt_index = pd.date_range('2022-01-01', periods=3, tz='UTC')
    result = is_datetimetz(dt_index)
    print("is_datetimetz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_datetimetz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()