from matplotlib.backends.backend_qt5agg import FigureCanvasQTAggBase, FigureCanvasQT
from matplotlib.figure import Figure
import inspect

class TestCanvas(FigureCanvasQTAggBase, FigureCanvasQT):
    pass

def main():
    fig = Figure()
    canvas = TestCanvas(fig)
    print("FigureCanvasQTAgg instance created:", canvas)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FigureCanvasQTAggBase))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()