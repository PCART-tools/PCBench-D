import pandas as pd
import inspect

def main():
    # Create a sample DataFrame
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    
    # Call the __iter__ method
    result = list(df.__iter__())
    print("__iter__ result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__iter__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()