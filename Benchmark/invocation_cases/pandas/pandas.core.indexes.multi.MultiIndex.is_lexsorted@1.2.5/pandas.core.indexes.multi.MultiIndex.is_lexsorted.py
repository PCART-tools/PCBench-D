import pandas as pd
import inspect

def main():
    # Create a MultiIndex
    arrays = [[1, 2, 2], ['red', 'blue', 'blue']]
    index = pd.MultiIndex.from_arrays(arrays, names=('number', 'color'))
    
    # Check if the MultiIndex is lexsorted
    result = index.is_lexsorted()
    print("is_lexsorted result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.MultiIndex.is_lexsorted))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()