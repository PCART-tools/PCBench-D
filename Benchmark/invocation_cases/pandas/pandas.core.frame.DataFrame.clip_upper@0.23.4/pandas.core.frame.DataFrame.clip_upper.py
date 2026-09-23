import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    result = df.clip_upper(4)
    print("clip_upper result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.clip_upper))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()