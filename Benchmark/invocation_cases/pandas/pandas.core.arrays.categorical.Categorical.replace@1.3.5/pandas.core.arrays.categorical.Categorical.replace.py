import pandas as pd
import inspect

def main():
    categories = pd.Categorical(['a', 'b', 'c', 'a'])
    result = categories.replace('a', 'd')
    print("replace result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Categorical.replace))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()