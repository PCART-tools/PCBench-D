import pandas as pd
import inspect

def main():
    index1 = pd.Index([1, 2, 3, 4])
    index2 = pd.Index([3, 4, 5, 6])
    result = index1.sym_diff(index2)
    print("sym_diff result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Index.sym_diff))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()