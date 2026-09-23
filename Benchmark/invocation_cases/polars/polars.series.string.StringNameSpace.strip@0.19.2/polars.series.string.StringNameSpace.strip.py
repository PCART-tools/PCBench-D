import polars as pl
import inspect

def main():
    # Create a DataFrame with a string column
    df = pl.DataFrame({
        "text": ["  hello  ", "  world  ", "  polars  "]
    })
    
    # Use the strip method from StringNameSpace
    stripped_series = df["text"].str.strip()
    print("Stripped result:", stripped_series)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df["text"].str.strip))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()