import pandas as pd
import numpy as np
import inspect
from pandas.io.date_converters import parse_all_fields

def main():
    # Provide all date components as separate integer arrays
    year = np.array([2020], dtype=object)
    month = np.array([12], dtype=object)
    day = np.array([9], dtype=object)
    hour = np.array([0], dtype=object)
    minute = np.array([0], dtype=object)
    second = np.array([0], dtype=object)

    result = parse_all_fields(year, month, day, hour, minute, second)
    print("parse_all_fields result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(parse_all_fields))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
