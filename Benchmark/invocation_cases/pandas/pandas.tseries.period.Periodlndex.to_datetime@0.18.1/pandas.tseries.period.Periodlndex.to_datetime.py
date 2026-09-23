import pandas as pd
import inspect
from pandas import PeriodIndex

def main():
    # Create a PeriodIndex
    period_index = pd.period_range('2022-01', periods=3, freq='M')
    
    # Convert PeriodIndex to datetime
    result = PeriodIndex.to_datetime(period_index)
    print("to_datetime result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PeriodIndex.to_datetime))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()