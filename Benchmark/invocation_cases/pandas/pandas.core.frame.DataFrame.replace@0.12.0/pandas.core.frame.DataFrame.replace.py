import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    result = df.replace(1, 100)
    print("replace result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.replace))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()