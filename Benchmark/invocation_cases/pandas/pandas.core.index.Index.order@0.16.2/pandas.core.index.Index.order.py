import pandas as pd
import inspect

def main():
    index = pd.Index([3, 1, 2])
    result = index.order()
    print("order result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Index.order))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()