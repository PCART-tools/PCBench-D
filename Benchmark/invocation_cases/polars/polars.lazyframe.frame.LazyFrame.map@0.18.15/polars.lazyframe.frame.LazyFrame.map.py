import polars as pl
import inspect

def main():
    # Create a LazyFrame
    data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
    lazy_df = pl.DataFrame(data).lazy()

    # Define a simple function to map
    def add_columns(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns((pl.col("a") + pl.col("b")).alias("sum"))

    # Use the apply function with the correct schema
    result = lazy_df.map(add_columns, predicate_pushdown=False, schema={"a": pl.Int64, "b": pl.Int64, "sum": pl.Int64}).collect()
    print("map result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.map))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()