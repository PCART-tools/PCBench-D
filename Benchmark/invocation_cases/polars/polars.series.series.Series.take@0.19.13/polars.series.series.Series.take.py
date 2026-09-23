import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [10, 20, 30, 40, 50])
    
    # Use the take method
    result = series.take([0, 2, 4])
    print("take result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.take))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()