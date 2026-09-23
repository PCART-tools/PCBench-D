import polars as pl
import inspect

def main():
    # Create two DataFrames for comparison
    df1 = pl.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    df2 = pl.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })

    # Call the frame_equal method
    result = df1.frame_equal(df2)
    print("frame_equal result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.frame_equal))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()