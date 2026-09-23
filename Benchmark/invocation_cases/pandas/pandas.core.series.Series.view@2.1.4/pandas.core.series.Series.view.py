import pandas as pd
import inspect

def main():
    s = pd.Series([1, 2, 3, 4])
    result = s.view()
    print("view result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.view))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()