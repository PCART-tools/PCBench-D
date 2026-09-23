import polars as pl
import inspect

def main():
    # Create a DataFrame with a JSON string column
    df = pl.DataFrame({
        "json_col": ['{"a": 1, "b": 2}', '{"a": 3, "b": 4}']
    })

    # Use the json_extract function
    result = df["json_col"].str.json_extract()
    print("json_extract result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["json_col"].str.json_extract))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()