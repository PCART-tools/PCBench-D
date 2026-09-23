import pandas as pd
import numpy as np
import inspect

def main():
    data = np.random.rand(2, 3, 4)
    panel = pd.Panel(data)
    result = panel._wrap_array(data, panel.axes)
    print("wrap_array result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.Panel._wrap_array))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()