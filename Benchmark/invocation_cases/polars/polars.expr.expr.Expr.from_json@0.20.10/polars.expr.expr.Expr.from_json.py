import polars as pl
import inspect
import io

def main():
    expr = (pl.col("a") * 2).alias("double")
    s = expr.meta.write_json()
    restored = pl.Expr.from_json(s)
    print(restored)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.from_json))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()