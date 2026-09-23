import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.parasite_axes import ParasiteAxesBase
from mpl_toolkits.axes_grid1 import host_subplot
from matplotlib.axes import Axes
import inspect


class MyParasiteAxes(ParasiteAxesBase, Axes):
    def __init__(self, parent_axes):
        super().__init__(parent_axes)


def main():
    fig = plt.figure()
    host = host_subplot(111)

    parasite = MyParasiteAxes(host)
    host.parasites.append(parasite)

    host.plot([0, 1, 2], [0, 1, 4])
    parasite.plot([0, 1, 2], [0, 2, 3])

    parasite.update_viewlim()
    print("update_viewlim called successfully via subclass")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(parasite.update_viewlim))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()