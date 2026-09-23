import inspect
from matplotlib.figure import Figure
from matplotlib.backend_bases import FigureCanvasBase

class MyCanvas(FigureCanvasBase):
    def __init__(self, figure):
        super().__init__(figure)


def main():
    fig = Figure()
    canvas = MyCanvas(fig)
    canvas.set_window_title("test")
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(canvas.set_window_title))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()