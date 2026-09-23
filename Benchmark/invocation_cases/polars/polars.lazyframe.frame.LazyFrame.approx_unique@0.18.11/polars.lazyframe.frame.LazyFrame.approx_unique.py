import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {"col1": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]}
    lazy_df = pl.DataFrame(data).lazy()

    # Call the approx_unique method
    result = pl.LazyFrame.approx_unique(lazy_df)
    print("approx_unique result:", result.collect())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.approx_unique))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()