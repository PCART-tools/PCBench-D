import pandas as pd
import numpy as np
import inspect

def main():
    df = pd.DataFrame({'A': [1, 2, 3]})
    arr = np.array([[10], [20], [30]])
    axes = (df.index, df.columns)
    result = df._wrap_array(arr, axes)

    print("Result of _wrap_array:")
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(df._wrap_array))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()