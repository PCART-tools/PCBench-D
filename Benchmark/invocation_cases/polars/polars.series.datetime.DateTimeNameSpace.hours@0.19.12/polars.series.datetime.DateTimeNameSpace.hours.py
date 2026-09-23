import polars as pl
import inspect
import datetime

def main():
    s = pl.Series(
        "d",
        [1_000_002, 3_000],
        dtype=pl.Duration("us"),
    )

    result = s.dt.hours()
    print(result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(s.dt.hours))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()