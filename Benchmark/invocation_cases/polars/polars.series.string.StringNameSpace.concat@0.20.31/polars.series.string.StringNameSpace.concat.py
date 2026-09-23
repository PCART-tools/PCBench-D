import polars as pl
import inspect

def main():
    # Create a Polars Series with string data
    series = pl.Series(["Hello", "World", "Polars"])
    
    # Use the StringNameSpace.concat method
    result = series.str.concat(", ")
    print("concat result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.str.concat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()