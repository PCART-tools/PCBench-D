import polars as pl
import inspect

def main():
    # Create a sample DataFrame
    df = pl.DataFrame({
        "a": [1, 2, 3, 4, 5],
        "b": [6, 7, 8, 9, 10]
    })
    
    # Use the take_every method
    result = df.take_every(2)
    print("take_every result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.DataFrame.take_every))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()