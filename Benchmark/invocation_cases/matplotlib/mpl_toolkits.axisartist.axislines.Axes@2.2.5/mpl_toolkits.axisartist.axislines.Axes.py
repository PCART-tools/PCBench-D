import matplotlib
matplotlib.use("Agg")  # Headless 环境适配

import matplotlib.pyplot as plt
import inspect

from mpl_toolkits.axisartist.axes_divider import Axes

def main():
    fig = plt.figure()
    ax = Axes(fig, [0.1, 0.1, 0.8, 0.8])  
    fig.add_axes(ax)

    print("Axes instance:", ax)
    print("Axes type:", type(ax))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Axes))
    except Exception as e:
        print(type(e).__name__, ":", e)

if __name__ == "__main__":
    main()
