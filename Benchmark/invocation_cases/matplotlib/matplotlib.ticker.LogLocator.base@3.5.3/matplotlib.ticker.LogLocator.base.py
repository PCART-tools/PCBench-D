import matplotlib.ticker as ticker
import inspect

def main():
    locator = ticker.LogLocator(base=10.0)
    print("LogLocator base:", locator.base(10))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.LogLocator.base))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()