import pandas as pd
import inspect
from pandas.core.generic import NDFrame

def main():
    data = {'A': 1, 'B': 2, 'C': 3}
    df = pd.Series(data)
    result = list(NDFrame.iterkv(df))
    print("iterkv result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(NDFrame.iterkv))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()