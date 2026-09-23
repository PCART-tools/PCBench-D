import pandas as pd
import inspect
from pandas.core.dtypes.common import is_extension_type

def main():
    data = pd.Series([1, 2, 3])
    result = is_extension_type(data)
    print("is_extension_type result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_extension_type))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()