import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {'name': ['Alice', 'Bob'], 'age': [25, 30]}
    lazy_df = pl.LazyFrame(data)

    # Write the LazyFrame to JSON format
    result = lazy_df.write_json()
    print("write_json result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.write_json))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()