import pandas as pd
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    result = df.as_matrix()
    print("as_matrix result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.as_matrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()