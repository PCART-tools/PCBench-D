import polars as pl
import inspect

def main():
    # Create a sample Series
    s = pl.Series(["apple", "banana", "cherry"])
    
    # Use the rjust method from StringNameSpace
    result = s.str.rjust(10, fill_char='*')
    print("rjust result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(s.str.rjust))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()