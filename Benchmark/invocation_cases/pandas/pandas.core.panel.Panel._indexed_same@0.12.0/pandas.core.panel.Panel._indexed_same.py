import pandas as pd
import numpy as np
import inspect

def main():
    data = np.random.rand(2, 3, 4)
    panel = pd.Panel(data)
    result = panel._indexed_same(panel)
    print("_indexed_same result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel._indexed_same))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()