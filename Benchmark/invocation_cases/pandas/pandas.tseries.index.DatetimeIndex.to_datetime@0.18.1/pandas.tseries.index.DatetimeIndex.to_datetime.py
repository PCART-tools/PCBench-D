import pandas as pd
import inspect

def main():
    dates = pd.date_range('20230101', periods=3)
    datetime_index = pd.DatetimeIndex(dates)
    result = datetime_index.to_datetime()
    print("to_datetime result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(datetime_index.to_datetime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()