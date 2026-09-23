import polars as pl
import inspect
from datetime import datetime

def main():
    # Create a DataFrame with a datetime column
    df = pl.DataFrame({
        "datetime": [
            datetime(2023, 1, 1, 12, 0, 0),
            datetime(2023, 1, 1, 12, 0, 1),
        ]
    })

    # Use the microseconds method
    result = df.select(
        pl.col("datetime")
        .diff()
        .dt.microseconds()
        .alias("microseconds")
    )
    print("microseconds result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("datetime").diff().dt.microseconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()