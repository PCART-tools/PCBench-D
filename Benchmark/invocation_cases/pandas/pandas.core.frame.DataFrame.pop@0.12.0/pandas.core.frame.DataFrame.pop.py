import pandas as pd
import inspect

def main():
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    result = df.pop('A')
    print("pop result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.pop))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()