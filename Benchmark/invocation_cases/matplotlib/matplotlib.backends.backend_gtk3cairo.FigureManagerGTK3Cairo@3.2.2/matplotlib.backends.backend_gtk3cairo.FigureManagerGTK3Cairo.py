import matplotlib.pyplot as plt
import inspect
from matplotlib.backends.backend_gtk3cairo import (
    FigureCanvasGTK3Cairo,
    FigureManagerGTK3Cairo,
)

def main():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    canvas = FigureCanvasGTK3Cairo(fig)
    manager = FigureManagerGTK3Cairo(canvas, 1)
    print("FigureManagerGTK3Cairo created:", manager)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FigureManagerGTK3Cairo))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
