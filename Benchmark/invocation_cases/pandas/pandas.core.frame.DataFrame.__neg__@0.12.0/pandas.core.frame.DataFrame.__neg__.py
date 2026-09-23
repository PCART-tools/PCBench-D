import pandas as pd
import inspect

def main():
    # Create a sample DataFrame
    df = pd.DataFrame([[1, -2], [-3, 4]], columns=["A", "B"])
    
    # Call the __neg__ method
    result = df.__neg__()
    print("Result of __neg__:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__neg__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()