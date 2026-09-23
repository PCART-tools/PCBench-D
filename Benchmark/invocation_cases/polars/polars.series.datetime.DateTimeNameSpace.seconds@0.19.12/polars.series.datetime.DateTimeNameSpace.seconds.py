import polars as pl
import inspect
from datetime import datetime, timedelta

def main():
    # Create datetime values manually to ensure correct dtype
    datetimes = [datetime(2023, 1, 1, 0, 0) + timedelta(minutes=15 * i) for i in range(5)]
    df = pl.DataFrame({
        "datetime": pl.Series(datetimes, dtype=pl.Datetime("ms"))
    })

    # Access the seconds from the datetime column
    seconds = (
        df["datetime"]
        .diff()
        .dt.seconds()
    )
    print("Seconds:", seconds)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["datetime"].diff().dt.seconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
