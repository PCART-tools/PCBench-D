import inspect
from pandas.core.common import UnsupportedFunctionCall

def main():
    try:
        raise UnsupportedFunctionCall("test UnsupportedFunctionCall")
    except UnsupportedFunctionCall as e:
        print("Exception:", type(e).__name__)
        print("Message:", e)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(UnsupportedFunctionCall))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()