import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [1, 2, 2, 3, 4, 4, 5])
    
    # Call the is_first method
    result = series.is_first()
    print("is_first result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.is_first))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()