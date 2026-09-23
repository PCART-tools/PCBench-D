import polars as pl
import inspect

def main():
    # Create a DataFrame with a list column
    df = pl.DataFrame(
        {
            "list_col": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        }
    )

    # Invoke ExprListNameSpace.count_match (polars 0.19.2 expects a scalar value)
    result = df.select(pl.col("list_col").list.count_match(5))
    print("count_match result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("list_col").list.count_match))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
