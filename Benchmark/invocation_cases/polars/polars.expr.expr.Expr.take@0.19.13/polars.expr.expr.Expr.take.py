import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "values": [10, 20, 30, 40, 50]
    })
    expr = pl.col("values").take([0, 2, 4])
    result = df.select(expr)
    print("take result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.take))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()