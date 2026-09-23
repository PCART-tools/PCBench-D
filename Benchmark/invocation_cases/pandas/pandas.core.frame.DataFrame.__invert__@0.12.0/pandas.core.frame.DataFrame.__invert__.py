import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [True, False, True], 'B': [False, True, False]})
    result = df.__invert__()
    print("Inverted DataFrame:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__invert__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()