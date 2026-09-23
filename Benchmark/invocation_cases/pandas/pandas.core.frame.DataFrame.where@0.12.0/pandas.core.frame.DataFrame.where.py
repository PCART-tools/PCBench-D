import pandas as pd
import numpy as np
import inspect

def main():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40]
    })
    condition = df > 2
    result = df.where(condition, -1)
    print("where result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.where))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()