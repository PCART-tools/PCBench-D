import matplotlib.ticker as ticker
import inspect

def main():
    formatter = ticker.LogFormatter()
    formatter.label_minor(10)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.LogFormatter.label_minor))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()