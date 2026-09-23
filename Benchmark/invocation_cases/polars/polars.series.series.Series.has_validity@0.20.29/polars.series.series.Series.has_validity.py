import polars as pl
import inspect

def main():
    # Create a Polars Series with some None values
    series = pl.Series("a", [1, None, 3, 4])
    result = series.has_validity()
    print("has_validity result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(series.has_validity))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()