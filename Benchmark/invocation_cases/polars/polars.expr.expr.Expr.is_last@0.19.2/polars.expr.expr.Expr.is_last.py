import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "group": ["A", "A", "B", "B"],
        "value": [1, 2, 3, 4]
    })

    # Use the is_last expression
    result = df.with_columns(pl.col("group").is_last().alias("is_last"))
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.is_last))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()