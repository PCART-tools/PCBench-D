import polars as pl
import inspect

def main():
    # Create a DataFrame with a list column
    df = pl.DataFrame({
        "numbers": [[1, 2, 3], [4, 5], [6]]
    })

    # Use the Expr.list method
    result = df.select(pl.Expr.list(pl.col("numbers")))
    print("list result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.list))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()