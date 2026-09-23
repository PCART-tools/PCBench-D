import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import inspect

def main():
    # Create a simple plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # Use OldScalarFormatter
    formatter = ticker.OldScalarFormatter()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ticker.OldScalarFormatter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()