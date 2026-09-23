import pandas as pd
import inspect

def main():
    # Create a Series
    s = pd.Series([1, 2, 3, 4])
    
    # Call the swapaxes method
    result = s.swapaxes(0, 0)
    print("swapaxes result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.swapaxes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()