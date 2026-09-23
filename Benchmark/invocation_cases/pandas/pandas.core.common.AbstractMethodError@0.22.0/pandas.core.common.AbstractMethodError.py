import pandas as pd
import inspect
from pandas.core.common import AbstractMethodError

def main():
    try:
        raise AbstractMethodError("This is a test error")
    except AbstractMethodError as e:
        print("Caught AbstractMethodError:", e)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(AbstractMethodError))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()