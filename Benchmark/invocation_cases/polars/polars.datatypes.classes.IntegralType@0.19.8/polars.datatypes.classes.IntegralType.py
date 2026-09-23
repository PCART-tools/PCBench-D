import polars as pl
import inspect
from polars.datatypes.classes import IntegralType

def main():
    class DummyIntegral(IntegralType):
        def __init__(self):
            super().__init__()

    obj = DummyIntegral()
    print(obj)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(IntegralType))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()