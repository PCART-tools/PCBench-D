import pandas as pd
import inspect

def main():
    # Create a sample DataFrame
    rng = pd.date_range('2021-01-01', periods=5, freq='T')
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5]}, index=rng)

    # Use TimeGrouper to group by 2-minute intervals
    grouper = pd.TimeGrouper(freq='2T')
    grouped = df.groupby(grouper).sum()
    print("Grouped result:\n", grouped)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.TimeGrouper))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()