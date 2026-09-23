import polars as pl
import inspect

def main():
    # Create a DataFrame with JSON data
    df = pl.DataFrame({
        "json_column": ['{"key": "value"}', '{"key": 42}', '{"key": true}']
    })

    # Correct usage of the json_extract method
    result = df.select(pl.col("json_column").str.json_extract())
    print("json_extract result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("json_column").str.json_extract))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()