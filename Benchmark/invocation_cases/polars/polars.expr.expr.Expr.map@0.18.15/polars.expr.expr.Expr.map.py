import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "numbers": [1, 2, 3, 4, 5]
    })

    # Use the Expr.map function
    result = df.select(
        pl.col("numbers").map(lambda x: x * 2)
    )
    print("map result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.map))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()