import polars as pl
import inspect

def main():
    # Create a Polars Series with string data
    series = pl.Series(["apple", "banana", "cherry"])
    
    # Use the ljust method from StringNameSpace
    result = series.str.ljust(10, '*')
    print("ljust result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.str.ljust))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()