import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "text": ["apple", "banana", "cherry"]
    })
    
    result = df.select(pl.col("text").str.rjust(10, " "))
    print("rjust result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("text").str.rjust))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()