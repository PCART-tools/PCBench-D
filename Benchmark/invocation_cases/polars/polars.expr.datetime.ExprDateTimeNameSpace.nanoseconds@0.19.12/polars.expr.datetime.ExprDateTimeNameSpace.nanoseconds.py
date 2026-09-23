import polars as pl
import inspect
from datetime import datetime

def main():
    # Create a DataFrame with a datetime column
    df = pl.DataFrame(
        {
            "datetime": pl.Series(
                [datetime(2023, 1, 1, 0, 0, 0, 123456)],
                dtype=pl.Datetime("ns"),
            )
        }
    )

    # Use the nanosecond method from ExprDateTimeNameSpace
    result = df.select(
        pl.col("datetime")
        .diff()
        .dt.nanoseconds()
    )
    print("nanoseconds result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("datetime").diff().dt.nanoseconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
