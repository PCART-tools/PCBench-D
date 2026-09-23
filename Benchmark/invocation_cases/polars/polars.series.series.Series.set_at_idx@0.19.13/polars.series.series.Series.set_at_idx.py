import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("a", [1, 2, 3, 4, 5])
    
    # Use the set_at_idx method
    result = series.set_at_idx(2, 10)
    print("set_at_idx result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.set_at_idx))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()