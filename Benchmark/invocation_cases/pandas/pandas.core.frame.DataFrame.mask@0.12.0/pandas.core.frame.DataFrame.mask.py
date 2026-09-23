import pandas as pd
import numpy as np
import inspect

def main():
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    mask = df > 2
    result = df.mask(mask)
    print("mask result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.DataFrame.mask))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()