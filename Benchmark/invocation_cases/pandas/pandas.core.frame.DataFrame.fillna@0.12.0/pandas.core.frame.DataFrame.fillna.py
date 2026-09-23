import pandas as pd
import inspect
import numpy as np

def main():
    df = pd.DataFrame({
        'A': [1, np.nan, 3],
        'B': [4, 5, np.nan]
    })
    result = df.fillna(0)
    print("fillna result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.fillna))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()