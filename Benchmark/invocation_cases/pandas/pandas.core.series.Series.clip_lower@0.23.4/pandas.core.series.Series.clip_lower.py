import pandas as pd
import inspect

def main():
    data = pd.Series([1, 2, 3, 4, 5])
    result = data.clip_lower(3)
    print("clip_lower result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.clip_lower))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()