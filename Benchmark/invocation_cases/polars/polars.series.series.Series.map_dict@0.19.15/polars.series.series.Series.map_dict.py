import polars as pl
import inspect

def main():
    # Create a sample Series
    series = pl.Series("numbers", [1, 2, 3, 4, 5])
    
    # Define a dictionary for mapping
    mapping_dict = {1: "one", 2: "two", 3: "three"}
    
    # Use the map_dict method
    result = series.map_dict(mapping_dict, default="unknown")
    print("map_dict result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.Series.map_dict))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()