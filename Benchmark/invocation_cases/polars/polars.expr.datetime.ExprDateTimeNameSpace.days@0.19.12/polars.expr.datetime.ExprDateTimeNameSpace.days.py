import polars as pl
import inspect
import datetime

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "datetime_col": [datetime.datetime(2023, 12, 1), datetime.datetime(2023, 12, 5), datetime.datetime(2023, 12, 9)]
    })

    # Extract the days component using ExprDateTimeNameSpace.dt.days
    result = df.select(
        (pl.col("datetime_col") - pl.lit(datetime.datetime(2023, 12, 1)))
            .dt.days()
    )
    print("days result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource((pl.col("datetime_col") - pl.lit(datetime.datetime(2023, 12, 1))).dt.days))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()