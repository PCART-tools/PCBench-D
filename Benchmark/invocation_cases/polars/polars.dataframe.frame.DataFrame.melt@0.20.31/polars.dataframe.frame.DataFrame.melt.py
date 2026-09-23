import polars as pl
import inspect

def main():
    df = pl.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": ["x", "y", "z"]
    })
    
    result = df.melt(id_vars="A", value_vars=["B", "C"])
    print("melt result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.melt))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()