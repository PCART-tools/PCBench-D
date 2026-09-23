import polars as pl
import inspect

def main():
    # Create a Polars Series with string data
    series = pl.Series(["apple", "banana", "cherry", "date"])
    
    # Use the count_match method from StringNameSpace
    result = series.str.count_match("a")
    print("count_match result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.str.count_match))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()