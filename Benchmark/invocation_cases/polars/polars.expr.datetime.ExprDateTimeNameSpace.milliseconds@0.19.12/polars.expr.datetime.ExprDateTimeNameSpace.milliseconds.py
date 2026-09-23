import polars as pl
import inspect
from datetime import datetime

def main():
    df = pl.DataFrame({"x": [1, 2, 3]})
    df = df.with_columns(
        pl.duration(milliseconds=123).alias("dur"),
        pl.duration(seconds=4, milliseconds=456).alias("dur2"),
        pl.duration(hours=1, minutes=2, seconds=3, milliseconds=789).alias("dur3"),
    )

    print("schema:", df.schema)
    result = df.select(
        pl.col("dur").dt.milliseconds(),
        pl.col("dur2").dt.milliseconds(),
        pl.col("dur3").dt.milliseconds(),
    )

    print("milliseconds result:")
    print(result)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("dur").dt.milliseconds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()