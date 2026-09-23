import polars as pl
import inspect

def main():
    df = pl.DataFrame(
        {
            "date": ["2025-12-09", "2025-12-10", "2025-12-11"]
        }
    )
    df = df.with_columns(
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")
    )

    df = df.with_columns(
        pl.col("date").cast(pl.Datetime)
    )
    result = df.select(
        pl.col("date").dt.datetime()
    )
    print(result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("date").dt.datetime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()