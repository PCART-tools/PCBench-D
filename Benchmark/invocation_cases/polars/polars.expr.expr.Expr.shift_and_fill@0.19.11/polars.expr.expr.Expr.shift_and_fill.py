import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "values": [1, 2, 3, 4, 5]
    })

    # Use the shift_and_fill method
    result = df.select(pl.col("values").shift_and_fill(periods=1, fill_value=0))
    print("shift_and_fill result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.shift_and_fill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()