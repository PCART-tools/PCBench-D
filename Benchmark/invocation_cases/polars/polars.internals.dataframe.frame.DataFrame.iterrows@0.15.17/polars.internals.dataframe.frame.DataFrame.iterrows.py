import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })

    # Use the iterrows method
    for row in pl.DataFrame.iterrows(df):
        print(row)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.iterrows))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()