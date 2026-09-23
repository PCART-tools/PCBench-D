import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    
    # Call the target API
    result = df.with_row_count(name="row_id")
    print("with_row_count result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.with_row_count))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()