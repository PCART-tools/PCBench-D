import matplotlib.pyplot as plt
from matplotlib.axes._subplots import SubplotBase
from matplotlib.axes import Axes
import inspect

class MySubplot(Axes, SubplotBase):
    _axes_class = Axes
    def __init__(self, fig, *args, **kwargs):
        SubplotBase.__init__(self, fig, *args, **kwargs)

def main():
    fig = plt.figure()
    gs = fig.add_gridspec(1, 1)
    spec = gs[0]

    ax = MySubplot(fig, spec)
    fig.add_axes(ax)
    ax.change_geometry(2, 2, 1)
    print("change_geometry result: Geometry changed to 2x2 grid, position 1")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ax.change_geometry))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()