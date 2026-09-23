import polars as pl
import inspect
import io

def main():
    lf = pl.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 25],
        }
    ).lazy()

    buffer = io.StringIO()
    lf.write_json(buffer)

    buffer.seek(0)
    lf_restored = pl.LazyFrame.read_json(buffer)

    print("Restored LazyFrame result:")
    print(lf_restored.collect())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.LazyFrame.read_json))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()