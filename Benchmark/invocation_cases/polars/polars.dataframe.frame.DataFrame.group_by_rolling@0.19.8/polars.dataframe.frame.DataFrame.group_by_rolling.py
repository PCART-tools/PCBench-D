import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "date": pl.date_range(
            start=pl.datetime(2023, 1, 1),
            end=pl.datetime(2023, 1, 10),
            interval="1d",
            eager=True
        ),
        "value": range(10)
    }).set_sorted("date")

    # Call the group_by_rolling method
    result = df.group_by_rolling(index_column="date", period="2d").agg(pl.col("value").sum())
    print("group_by_rolling result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df.group_by_rolling))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
