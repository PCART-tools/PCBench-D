import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })

    # Define a function to apply
    def add_columns(row):
        return row[0] + row[1]

    # Apply the function to the DataFrame
    result = df.apply(add_columns, return_dtype=pl.Int64)
    print("apply result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df.apply))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()