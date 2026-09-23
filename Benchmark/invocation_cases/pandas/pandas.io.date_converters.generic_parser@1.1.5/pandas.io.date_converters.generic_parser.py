import pandas as pd
import inspect
from pandas.io.date_converters import generic_parser

def main():

    def parse_sum(a, b):
        return a + b
    col1 = [1, 2, 3]
    col2 = [10, 20, 30]
    result = generic_parser(parse_sum, col1, col2)
    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(generic_parser))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()