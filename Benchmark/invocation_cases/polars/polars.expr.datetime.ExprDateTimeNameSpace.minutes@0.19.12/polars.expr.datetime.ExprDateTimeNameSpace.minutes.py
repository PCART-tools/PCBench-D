import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "datetime": ["2025-12-09 08:49:51", "2025-12-09 09:49:51"]
    }).with_columns(pl.col("datetime").str.strptime(pl.Datetime))

    result = (
        df.with_columns(
            pl.col("datetime")
            .diff()
            .dt.minutes()
            .alias("minutes")
        )
        .select("minutes")
    )
    print("minutes result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("datetime").diff().dt.minutes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()