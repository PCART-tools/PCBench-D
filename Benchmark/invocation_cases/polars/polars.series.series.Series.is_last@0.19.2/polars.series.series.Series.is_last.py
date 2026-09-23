import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [1, 2, 2, 3, 4, 4, 5])
    
    # Call the is_last method
    result = series.is_last()
    print("is_last result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.is_last))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()