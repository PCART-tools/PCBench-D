import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    expr = pl.col("numbers").take_every(2)
    result = df.select(expr)
    print("take_every result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.take_every))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()