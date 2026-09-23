import polars as pl
import inspect

def main():
    # Create a DataFrame
    df = pl.DataFrame({
        "a": [1, 2, 2, 3],
        "b": [4, 5, 6, 7]
    })

    # Use the groupby method
    grouped = df.groupby("a").agg(pl.col("b").sum())
    print("groupby result:\n", grouped)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.groupby))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()