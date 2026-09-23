import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    result = df.__contains__('A')
    print("__contains__ result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__contains__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()