import inspect
from pandas.core.daterange import DateRange
from pandas.tseries.offsets import Day
import pandas as pd

def main():
    dr = DateRange(
        start="2022-01-01",
        end="2022-01-10",
        offset=Day(),
        name="test_range"
    )

    print("DateRange result:", dr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DateRange))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()