import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "category": ["A", "B", "C", "A", "B"]
    })

    # Define a mapping dictionary
    mapping = {"A": 1, "B": 2, "C": 3}

    # Use map_dict on an expression
    result = df.with_columns(
        pl.col("category").map_dict(mapping).alias("mapped_category")
    )
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.map_dict))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()