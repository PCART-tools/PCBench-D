import polars as pl
import inspect

def main():
    # Create a DataFrame with sample data
    df = pl.DataFrame({
        "values": [1, 2, 3, 4, 5, 6]
    })

    # Define a custom function for rolling_apply
    def custom_func(window):
        return window.sum()

    # Use rolling_apply on the 'values' column
    result = df.select(
        pl.col("values").rolling_apply(custom_func, window_size=3)
    )
    print("rolling_apply result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.rolling_apply))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()