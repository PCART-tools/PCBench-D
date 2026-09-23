import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {
        "name": ["Alice", "Bob", "Alice", "Bob"],
        "age": [25, 30, 25, 30],
        "score": [85, 90, 95, 80]
    }
    lazy_df = pl.LazyFrame(data)

    # Call the groupby method
    grouped = lazy_df.groupby("name").agg(pl.col("score").mean())
    print("groupby result:", grouped.collect())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.groupby))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()