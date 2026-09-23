import pandas as pd
import inspect

def main():
    data = pd.Series(['1', '2', '3', '4.5'])
    result = data.convert_objects(convert_numeric=True)
    print("convert_objects result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.convert_objects))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()