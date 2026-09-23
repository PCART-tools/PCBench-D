import pandas as pd
import inspect

def main():
    # Create a MultiIndex DataFrame
    index = pd.MultiIndex.from_tuples([('a', 1), ('a', 2), ('b', 1), ('b', 2)])
    df = pd.DataFrame({'values': [10, 20, 15, 25]}, index=index)
    
    # Call the sortlevel method
    sorted_df = df.sortlevel(level=0)
    print("sortlevel result:\n", sorted_df)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.sortlevel))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()