import matplotlib.ticker as ticker
import inspect

def main():
    locator = ticker.LogLocator(base=10.0, subs=[2.0, 3.0], numticks=10)
    result = locator.subs(None)
    print("LogLocator subs:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(locator.subs))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()