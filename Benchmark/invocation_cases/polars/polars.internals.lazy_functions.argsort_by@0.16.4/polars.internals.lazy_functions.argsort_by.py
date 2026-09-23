import polars as pl
import inspect

def main():
    # Create test data
    df = pl.DataFrame({
        "col1": [3, 1, 2],
        "col2": [9, 7, 8]
    })

    # Call the target API
    result = pl.argsort_by([df["col1"], df["col2"]], reverse=[True, False])
    print("argsort_by result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.argsort_by))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()