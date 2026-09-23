import polars as pl
import inspect

def main():
    # Create a Series with string numbers
    series = pl.Series(["1", "2", "3", "4"])
    
    # Use the parse_int method from StringNameSpace
    result = series.str.parse_int(strict=False)
    print("parse_int result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.str.parse_int))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()