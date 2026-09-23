import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "text_column": ["apple", "banana", "apple pie", "banana split", "apple"]
    })

    # Use the count_match method to count occurrences of "apple" in the text_column
    result = df.select(
        pl.col("text_column").str.count_match("apple").alias("apple_count")
    )
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.col("text_column").str.count_match))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()