import polars as pl
import inspect

def main():
    s = pl.Series(
        "list_column",
        [[1, 2, 3], [4, 5, 6], [5, 5, 5], []]
    )

    result = s.list.count_match(5)
    print("count_match result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(s.list.count_match))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
