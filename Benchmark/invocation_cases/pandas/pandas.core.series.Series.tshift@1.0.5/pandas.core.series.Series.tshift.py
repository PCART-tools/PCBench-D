import pandas as pd
import inspect

def main():
    # Create a time series with a date range
    date_range = pd.date_range(start='2020-01-01', periods=5, freq='D')
    series = pd.Series([1, 2, 3, 4, 5], index=date_range)
    
    # Call the tshift method
    result = series.tshift(1)
    print("tshift result:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.tshift))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()