import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    state = df.__getstate__()
    print("__getstate__ result:", state)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.__getstate__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()