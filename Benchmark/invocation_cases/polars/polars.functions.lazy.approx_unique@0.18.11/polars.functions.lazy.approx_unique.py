import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "values": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    })

    lazy_df = df.lazy()
    result = lazy_df.select(pl.approx_unique("values")).collect()
    print("approx_unique result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.approx_unique))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()