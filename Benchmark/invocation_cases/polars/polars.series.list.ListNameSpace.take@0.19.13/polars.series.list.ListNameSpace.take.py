import polars as pl
import inspect

def main():
    s = pl.Series("lists", [[1, 2, 3], [4, 5], [6, 7, 8, 9]])
    result = s.list.take(1)
    print("take result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(s.list.take))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
