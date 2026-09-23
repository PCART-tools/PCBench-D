import polars as pl
import inspect

def main():
    # Toggle the string cache
    result = pl.string_cache.toggle_string_cache(True)
    print("toggle_string_cache result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.string_cache.toggle_string_cache))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()