import pandas as pd
import inspect

def main():
    data = {'A': ['1', '2', '3'], 'B': ['4.0', '5.1', '6.2']}
    df = pd.DataFrame(data)
    result = df.convert_objects(convert_numeric=True)
    print("convert_objects result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.convert_objects))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()