import pandas as pd
import inspect

def main():
    # Create a DataFrame
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    
    # Access a column using __getattr__
    result = df.__getattr__('A')
    print("DataFrame column accessed using __getattr__:", result.tolist())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__getattr__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()