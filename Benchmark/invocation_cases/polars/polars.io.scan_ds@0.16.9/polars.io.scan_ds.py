import polars as pl
import inspect

def main():
    # Simulate a DataFrame to use with scan_ds
    df = pl.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })

    # Use the scan_ds function
    result = pl.scan_ds(df)
    print("scan_ds result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.scan_ds))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()