import polars as pl
import inspect
from datetime import datetime, timedelta

def main():
    # Create a DataFrame with a datetime column using concrete Python datetimes
    datetimes = [datetime(2023, 1, 1) + timedelta(hours=i) for i in range(25)]
    df = pl.DataFrame(
        {
            "datetime": pl.Series(datetimes, dtype=pl.Datetime("ms"))
        }
    )

    # Access the milliseconds component
    milliseconds = (
        df["datetime"]
        .diff()
        .dt.milliseconds()
    )
    print("Milliseconds:", milliseconds)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["datetime"].diff().dt.milliseconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
