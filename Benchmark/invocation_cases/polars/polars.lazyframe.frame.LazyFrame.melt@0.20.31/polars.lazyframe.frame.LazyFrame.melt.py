import polars as pl
import inspect

def main():
    # Create a LazyFrame with sample data
    data = {
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9]
    }
    lazy_df = pl.LazyFrame(data)

    # Call the melt method
    melted_df = lazy_df.melt(id_vars=["A"], value_vars=["B", "C"])
    print("melt result:", melted_df.collect())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.melt))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()