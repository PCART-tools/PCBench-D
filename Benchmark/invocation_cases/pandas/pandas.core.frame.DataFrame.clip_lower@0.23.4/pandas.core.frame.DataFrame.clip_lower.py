import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    result = df.clip_lower(2)
    print("clip_lower result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.clip_lower))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()