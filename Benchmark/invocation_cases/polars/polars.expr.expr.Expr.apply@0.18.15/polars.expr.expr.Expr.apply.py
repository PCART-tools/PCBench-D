import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "values": [1, 2, 3, 4, 5]
    })

    # Use the Expr.apply method
    result = df.select(
        pl.col("values").apply(lambda x: x * 2)
    )
    print("apply result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.apply))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()