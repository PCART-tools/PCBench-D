import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.parasite_axes import (
    ParasiteAxesAuxTransBase,
    ParasiteAxesBase,
)
from matplotlib.axes import Axes
from matplotlib.transforms import IdentityTransform
import inspect


class MyParasiteAxes(ParasiteAxesAuxTransBase, ParasiteAxesBase,Axes):
    def __init__(self, parent_axes):
        super().__init__(
            parent_axes=parent_axes,
            aux_transform=IdentityTransform(),
            viewlim_mode=None
        )


def main():
    fig, host = plt.subplots()
    parasite = MyParasiteAxes(host)

    print("Instance:", parasite)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ParasiteAxesAuxTransBase))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()