import matplotlib.backend_bases as mbb
import inspect
from matplotlib.figure import Figure

def main():
    class CustomCanvas(mbb.FigureCanvasBase):
        pass

    fig = Figure()
    canvas = CustomCanvas(fig)
    result = canvas.get_window_title()
    print("get_window_title result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbb.FigureCanvasBase.get_window_title))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()