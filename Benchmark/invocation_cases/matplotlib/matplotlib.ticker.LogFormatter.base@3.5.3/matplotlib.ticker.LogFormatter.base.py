import matplotlib.ticker as ticker
import inspect

def main():
    log_formatter = ticker.LogFormatter()
    log_formatter.base(10)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.LogFormatter.base))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()