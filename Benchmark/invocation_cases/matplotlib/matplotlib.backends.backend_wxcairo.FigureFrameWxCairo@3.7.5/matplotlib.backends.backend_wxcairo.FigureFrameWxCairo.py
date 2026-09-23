import matplotlib
import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxcairo import FigureFrameWxCairo
import inspect

def main():
    app = wx.App(False)
    fig = Figure()
    frame = FigureFrameWxCairo(1, fig)
    print("FigureFrameWxCairo instance created:", frame)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FigureFrameWxCairo))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()