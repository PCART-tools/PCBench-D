import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "numbers": ["10", "20", "30", "invalid"]
    })
    
    result = df.select(pl.col("numbers").str.parse_int(10, strict=False))
    print("parse_int result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("numbers").str.parse_int))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()