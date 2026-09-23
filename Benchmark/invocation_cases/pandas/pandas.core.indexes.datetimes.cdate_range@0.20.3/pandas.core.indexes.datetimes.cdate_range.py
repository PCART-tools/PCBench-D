import pandas as pd
import inspect
import pandas.core.indexes.datetimes as datetimes

def main():
    result = datetimes.cdate_range("2023-01-01", periods=5)
    print("cdate_range result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(datetimes.cdate_range))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
