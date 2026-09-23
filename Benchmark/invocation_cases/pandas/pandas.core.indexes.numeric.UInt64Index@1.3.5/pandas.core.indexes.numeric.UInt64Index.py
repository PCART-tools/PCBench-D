import pandas as pd
import inspect

def main():
    data = [1, 2, 3, 4, 5]
    index = pd.UInt64Index(data)
    print("UInt64Index:", index)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.UInt64Index))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()