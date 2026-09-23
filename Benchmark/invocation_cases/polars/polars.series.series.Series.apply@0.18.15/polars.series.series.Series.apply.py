import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [1, 2, 3, 4, 5])
    
    # Apply a lambda function to double the values
    result = series.apply(lambda x: x * 2)
    print("apply result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.apply))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()