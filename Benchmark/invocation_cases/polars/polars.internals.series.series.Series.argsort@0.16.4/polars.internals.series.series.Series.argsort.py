import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("values", [3, 1, 2, 4])
    
    # Call the argsort method
    result = series.argsort()
    print("argsort result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.argsort))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()