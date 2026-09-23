import pandas as pd
import numpy as np
import inspect
from pandas.core.arrays import ExtensionArray

class MyExtensionArray(ExtensionArray):
    def __init__(self, data):
        self.data = np.array(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]


def main():
    my_array = MyExtensionArray([1, 2, 3, 4])
    result = my_array._formatting_values()
    print("_formatting_values result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ExtensionArray._formatting_values))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()