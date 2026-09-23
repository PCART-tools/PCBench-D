import polars as pl
import inspect
from datetime import datetime

def main():
    # Create a DataFrame with a datetime column using a proper dtype
    df = pl.DataFrame(
        {
            "datetime": pl.Series(
                [
                    datetime(2023, 1, 1, 12, 0, 30),
                    datetime(2023, 1, 1, 13, 15, 45),
                ],
                dtype=pl.Datetime("ms"),
            )
        }
    )

    # Extract the seconds from the datetime column
    result = df.with_columns(
        pl.col("datetime")
        .diff()
        .dt.seconds()
        .alias("seconds")
    )
    print("seconds result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("datetime").diff().dt.seconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
