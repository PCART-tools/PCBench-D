import matplotlib
import inspect
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureFrameWxAgg,FigureCanvasWxAgg
import wx

def main():
    app = wx.App(False)
    figure = Figure()
    ax = figure.add_subplot(111)
    ax.plot([1, 2, 3], [3, 2, 5])
    frame = FigureFrameWxAgg(num=1,fig=figure,canvas_class=FigureCanvasWxAgg)
    frame.Show()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FigureFrameWxAgg))
    except Exception as e:
        print(type(e).__name__)

    # app.MainLoop()

if __name__ == "__main__":
    main()