import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "col1": ["Hello", None, "World"],
    })

    result = df.select(
        pl.col("col1")
          .str.concat("-", ignore_nulls=True)
          .alias("concat_result")
    )
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("col1").str.concat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()