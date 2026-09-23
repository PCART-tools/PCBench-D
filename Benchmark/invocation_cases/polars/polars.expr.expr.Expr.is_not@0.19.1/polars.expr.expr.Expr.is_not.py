import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "values": [1, None, 3, None, 5]
    })

    # 构造一个 Boolean 表达式，再使用 is_not
    expr = pl.col("values").is_not_null().is_not()

    result = df.select(expr)
    print("is_not result:\n", result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Expr.is_not))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()