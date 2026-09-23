import pandas as pd
import numpy as np
import inspect

def main():
    data = np.random.rand(2, 3, 4)
    panel = pd.Panel(data)
    result = panel.__invert__()
    print("Inverted Panel:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel.__invert__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()