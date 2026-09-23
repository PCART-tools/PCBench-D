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
    geometry = ax.get_geometry()
    print("get_geometry result:", geometry)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ax.get_geometry))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()