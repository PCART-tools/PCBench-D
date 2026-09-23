import pandas as pd
import inspect
import numpy as np

def main():
    data = pd.Series([1, 2, 3, 4, 5], dtype=float)
    condition = data > 2
    result = data.where(condition)
    print("where result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Series.where))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()