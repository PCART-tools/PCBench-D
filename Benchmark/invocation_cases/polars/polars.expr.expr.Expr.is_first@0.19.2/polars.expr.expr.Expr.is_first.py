import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "group": ["A", "A", "B", "B", "C"],
        "value": [1, 2, 3, 4, 5]
    })

    # Use the is_first expression
    result = df.with_columns(pl.col("group").is_first().alias("is_first"))
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.is_first))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()