import polars as pl
import inspect

def main():
    # Simulate input for the function
    idx = 5
    result = pl.utils.meta.get_idx_type()
    print("get_idx_type result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.utils.meta.get_idx_type))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()