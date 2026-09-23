import pandas as pd
import inspect
from pandas.io.json import json_normalize

def main():
    data = [
        {'id': 1, 'name': 'John', 'info': {'age': 30, 'city': 'New York'}},
        {'id': 2, 'name': 'Jane', 'info': {'age': 25, 'city': 'Chicago'}}
    ]

    result = json_normalize(data)
    print("json_normalize result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(json_normalize))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
