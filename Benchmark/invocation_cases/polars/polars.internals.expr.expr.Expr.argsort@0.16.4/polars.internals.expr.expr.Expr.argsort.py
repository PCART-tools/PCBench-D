import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "values": [3, 1, 2]
    })

    # Use the argsort method on an expression
    result = df.select(pl.col("values").argsort())
    print("argsort result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("values").argsort))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()