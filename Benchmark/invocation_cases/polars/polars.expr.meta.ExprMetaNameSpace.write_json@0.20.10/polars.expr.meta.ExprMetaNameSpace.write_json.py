import polars as pl
import inspect

def main():
    expr = pl.col("name")

    # ✅ 调用 ExprMetaNameSpace.write_json
    json_str = expr.meta.write_json()
    print("Expr meta write_json result:")
    print(json_str)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(expr.meta.write_json))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()