import pandas as pd
import inspect
from pandas.core.reshape.merge import MergeError

def main():
    try:
        raise MergeError("test error")
    except MergeError as e:
        print("Caught MergeError:", e)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MergeError))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()