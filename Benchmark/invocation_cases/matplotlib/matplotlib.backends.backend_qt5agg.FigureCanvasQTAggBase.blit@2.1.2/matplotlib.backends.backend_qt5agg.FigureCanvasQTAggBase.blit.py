import matplotlib.backends.backend_qt5agg as backend_qt5agg
import numpy as np
import inspect
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication([])
    fig = Figure()
    canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
    canvas.draw()

    # Create a random image to blit
    image = np.random.rand(10, 10)
    # Make sure to draw the image using imshow before blitting
    ax = fig.add_subplot(111)
    ax.imshow(image, aspect='auto')
    canvas.draw()
    backend_qt5agg.FigureCanvasQTAggBase.blit(canvas,ax.bbox)
    print("blit called successfully")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(backend_qt5agg.FigureCanvasQTAggBase.blit))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()