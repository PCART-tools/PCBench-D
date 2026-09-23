import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "a": [1, 2, 3, 4],
        "b": [5, 6, 7, 8]
    })
    result = df.shift_and_fill(periods=1, fill_value=0)
    print("shift_and_fill result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.shift_and_fill))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()