import pandas as pd
import inspect

def main():
    items = [('A', [1, 2, 3]), ('B', [4, 5, 6])]
    df = pd.DataFrame.from_items(items)
    print("DataFrame from_items result:\n", df)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.from_items))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()