import polars as pl
import inspect

def main():
    # Create a DataFrame with a string column
    df = pl.DataFrame({
        "text": ["apple", "banana", "cherry"]
    })

    # Use the ljust method from ExprStringNameSpace
    result = df.select(pl.col("text").str.ljust(10))
    print("ljust result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("text").str.ljust))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()