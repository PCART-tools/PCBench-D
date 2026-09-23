import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    # Use the take_every method
    result = series.take_every(2)
    print("take_every result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.take_every))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()