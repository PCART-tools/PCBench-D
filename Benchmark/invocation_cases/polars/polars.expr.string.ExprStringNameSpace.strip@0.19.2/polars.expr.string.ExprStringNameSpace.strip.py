import polars as pl
import inspect

def main():
    # Create a DataFrame with a string column
    df = pl.DataFrame({
        "text": ["  hello  ", "  world  ", "  polars  "]
    })

    # Use the strip method from ExprStringNameSpace
    result = df.select(pl.col("text").str.strip())
    print("strip result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("text").str.strip))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()