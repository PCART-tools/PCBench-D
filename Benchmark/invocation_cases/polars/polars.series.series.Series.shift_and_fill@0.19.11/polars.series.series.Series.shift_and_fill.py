import polars as pl
import inspect

def main():
    # Create a sample Series
    s = pl.Series("a", [1, 2, 3, 4, 5])
    
    # Call the shift_and_fill method
    result = s.shift_and_fill(periods=2, fill_value=0)
    print("shift_and_fill result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.shift_and_fill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()