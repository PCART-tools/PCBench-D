import polars as pl
import inspect
from datetime import datetime, timedelta

def main():
    # Manually create datetime data to avoid deprecated `date_range` in 0.19.12
    datetimes = [datetime(2023, 1, 1, 0, 0) + timedelta(minutes=15 * i) for i in range(5)]
    df = pl.DataFrame({
        "datetime": pl.Series(datetimes, dtype=pl.Datetime("ms"))
    })

    # Access the minutes from the datetime column
    minutes = (
        df["datetime"]
        .diff()
        .dt.minutes()
    )
    print("Minutes:", minutes)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["datetime"].diff().dt.minutes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
