import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import axes_divider
import inspect

def main():
    fig = plt.figure()
    ax_divider = axes_divider.Axes(fig, [0.1, 0.1, 0.8, 0.8])
    fig.add_axes(ax_divider)
    print("Axes divider created:", ax_divider)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(axes_divider.Axes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
