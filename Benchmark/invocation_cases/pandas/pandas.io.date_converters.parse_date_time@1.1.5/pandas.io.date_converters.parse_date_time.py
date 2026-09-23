import pandas as pd
import numpy as np
import inspect
from pandas.io.date_converters import parse_date_time

def main():
    date_col = np.array(["2025-12-09"], dtype=object)
    time_col = np.array(["07:52:35"], dtype=object)

    result = parse_date_time(date_col, time_col)
    print("parse_date_time result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(parse_date_time))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()