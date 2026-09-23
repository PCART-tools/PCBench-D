import pandas as pd
import inspect

def main():
    idx1 = pd.Index([1, 2, 3, 4, 5])
    idx2 = pd.Index([0, 1, 2, 3, 4])
    result = idx1.diff(idx2)
    print("diff result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Index.diff))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()