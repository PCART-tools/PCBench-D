import pandas as pd
import inspect

def main():
    df = pd.DataFrame([[1, 2], [3, 4]], columns=['A', 'B'])
    result = df.applymap(lambda x: x * 2)
    print("applymap result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.applymap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()