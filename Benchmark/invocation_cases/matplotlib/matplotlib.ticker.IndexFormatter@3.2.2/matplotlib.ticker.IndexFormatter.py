import matplotlib.ticker as ticker
import inspect

def main():
    labels = ['A', 'B', 'C', 'D']
    formatter = ticker.IndexFormatter(labels)
    index = 2
    result = formatter(index)
    print("IndexFormatter result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.IndexFormatter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()