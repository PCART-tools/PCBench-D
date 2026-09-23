import polars as pl
import inspect

def main():
    # Create a LazyFrame
    data = {"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
    lazy_df = pl.LazyFrame(data)

    # Use with_row_count
    result = lazy_df.with_row_count("row_id").collect()
    print("with_row_count result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.with_row_count))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()