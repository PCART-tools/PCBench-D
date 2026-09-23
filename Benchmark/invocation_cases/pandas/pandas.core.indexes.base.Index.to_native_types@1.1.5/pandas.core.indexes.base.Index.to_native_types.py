import pandas as pd
import inspect

def main():
    idx = pd.Index([1, 2, 3, 4])
    result = idx.to_native_types()
    print("to_native_types result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Index.to_native_types))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()