import pandas as pd
import inspect

def main():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })
    
    # Use the filter method to select columns
    result = df.filter(items=['A', 'C'])
    print("filter result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.filter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()