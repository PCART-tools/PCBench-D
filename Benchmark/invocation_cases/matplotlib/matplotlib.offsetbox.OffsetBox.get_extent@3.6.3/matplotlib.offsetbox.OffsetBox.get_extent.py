import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetBox
from matplotlib.transforms import Bbox
import inspect


class DummyOffsetBox(OffsetBox):
    def get_extent_offsets(self, renderer):
        return 100.0, 50.0, 0.0, 0.0, []
    def _get_bbox_and_child_offsets(self, renderer):
        bbox = Bbox.from_bounds(0.0, 0.0, 100.0, 50.0)
        offsets = []
        return bbox, offsets

def main():
    fig, ax = plt.subplots()
    box = DummyOffsetBox()
    box.set_figure(fig)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    extent = OffsetBox.get_extent(box, renderer)
    print("get_extent result:", extent)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(OffsetBox.get_extent))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
