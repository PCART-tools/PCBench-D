import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {"a": [1, 2, 3, 4, 5], "b": [6, 7, 8, 9, 10]}
    lazy_df = pl.LazyFrame(data)

    # Call the take_every method
    result = lazy_df.take_every(2).collect()
    print("take_every result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.take_every))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()