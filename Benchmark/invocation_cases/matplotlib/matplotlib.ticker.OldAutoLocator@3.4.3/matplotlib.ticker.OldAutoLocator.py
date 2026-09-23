import matplotlib.ticker as ticker
import inspect
import matplotlib.pyplot as plt

def main():
    # Create a plot to use the OldAutoLocator
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 4, 9])

    # Use OldAutoLocator
    locator = ticker.OldAutoLocator()
    ax.xaxis.set_major_locator(locator)

    # Output the result of using OldAutoLocator
    print("OldAutoLocator result:", ax.xaxis.get_major_locator())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.OldAutoLocator))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()