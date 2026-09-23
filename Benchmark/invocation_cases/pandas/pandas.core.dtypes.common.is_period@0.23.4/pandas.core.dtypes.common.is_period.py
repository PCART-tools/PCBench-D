import pandas as pd
import numpy as np
import inspect
from pandas.core.dtypes.common import is_period

def main():
    period_data = pd.Period('2022-01', freq='M')
    result = is_period(period_data)
    print("is_period result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_period))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()