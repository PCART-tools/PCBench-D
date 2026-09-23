import polars as pl
import inspect
from datetime import datetime, timedelta

def main():
    # Create a DataFrame with a datetime column using concrete Python datetimes
    datetimes = [datetime(2025, 1, 1) + timedelta(hours=i) for i in range(25)]
    df = pl.DataFrame(
        {
            "datetime": pl.Series(datetimes, dtype=pl.Datetime("ms"))
        }
    )

    # Use the hour method from ExprDateTimeNameSpace
    result = df.select(
        (pl.col("datetime") - pl.col("datetime").first())
        .dt.hours()
        .alias("hours")
    )
    print("hours result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource((pl.col("datetime") - pl.col("datetime").first()).dt.hours))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
