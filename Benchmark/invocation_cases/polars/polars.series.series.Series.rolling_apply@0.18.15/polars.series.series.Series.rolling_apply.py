import polars as pl
import inspect

def main():
    # Create a sample Series
    s = pl.Series("values", [1, 2, 3, 4, 5, 6])

    # Define a simple function to apply
    def sum_func(window):
        return window.sum()

    # Use rolling_apply with a window size of 3
    result = s.rolling_apply(sum_func, window_size=3)
    print("rolling_apply result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.rolling_apply))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()