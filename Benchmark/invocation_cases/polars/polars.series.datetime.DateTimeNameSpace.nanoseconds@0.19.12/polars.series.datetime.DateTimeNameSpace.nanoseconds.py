import polars as pl
import inspect
from datetime import datetime

def main():
    # Create a sample DataFrame with a datetime column
    df = pl.DataFrame({
        "datetime": [datetime(2023, 1, 1, 12, 0, 0), datetime(2023, 1, 2, 13, 30, 0)]
    }).with_columns(pl.col("datetime").cast(pl.Datetime))

    # Access the nanoseconds from the datetime column
    nanoseconds = (
        df["datetime"]
        .diff()
        .dt.nanoseconds()
    )
    print("Nanoseconds result:", nanoseconds)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["datetime"].diff().dt.nanoseconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()