import polars as pl
import inspect

def main():
    series1 = pl.Series("a", [1, 2, 3])
    series2 = pl.Series("b", [1, 2, 3])
    result = series1.series_equal(series2)
    print("series_equal result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.series_equal))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()