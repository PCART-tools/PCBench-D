import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {
        "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "value": [10, 20, 30, 40]
    }
    lf = pl.LazyFrame(data).with_columns(pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")).set_sorted("date")

    # Call the group_by_rolling method
    result = lf.group_by_rolling(index_column="date", period="2d").agg(pl.col("value").sum())
    print("group_by_rolling result:", result.collect())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.group_by_rolling))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()