import polars as pl
import inspect
from datetime import datetime, timedelta

def main():
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(6)]
    s = pl.Series("date", dates, dtype=pl.Datetime)
    result = s.dt.datetime()
    print("DateTimeNameSpace.datetime result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(s.dt.datetime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
