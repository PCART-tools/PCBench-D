import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "a": [1, 2, 3, 4],
        "b": [5, 6, 7, 8]
    })

    # ✅ 关键：直接调用 Expr.where
    expr = pl.col("b").where(pl.col("a") > 2).fill_null(0)
    print(expr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.where))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()