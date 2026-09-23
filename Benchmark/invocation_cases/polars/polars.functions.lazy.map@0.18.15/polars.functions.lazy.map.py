import polars as pl
import inspect

def main():
    df = pl.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
    )
    expr = pl.map(
        exprs=[pl.col("a"), pl.col("b")],
        function=lambda s: s[0] + s[1],
        return_dtype=pl.Int64,
    ).alias("a_plus_b")

    result = df.with_columns(expr)

    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.map))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()