import inspect
from pandas.tseries.converter import register

def main():
    register()
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(register))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()