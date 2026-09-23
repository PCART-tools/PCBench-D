import matplotlib
import inspect
import matplotlib.figure
from matplotlib.backends.backend_gtk3agg import FigureManagerGTK3Agg, FigureCanvasGTK3Agg

def main():
    # Create a simple figure to use with FigureManagerGTK3Agg
    fig = matplotlib.figure.Figure()
    canvas = FigureCanvasGTK3Agg(fig)
    manager = FigureManagerGTK3Agg(canvas, 1)
    print("FigureManagerGTK3Agg created:", manager)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FigureManagerGTK3Agg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()