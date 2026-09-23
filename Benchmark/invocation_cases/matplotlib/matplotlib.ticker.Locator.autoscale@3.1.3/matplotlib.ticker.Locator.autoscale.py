import matplotlib.ticker as ticker
import inspect
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots()
    locator = ticker.MaxNLocator()
    ax.xaxis.set_major_locator(locator)
    
    ax.plot(range(10))
    plt.draw()

    result = ticker.Locator.autoscale(locator)
    print("autoscale result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.Locator.autoscale))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()