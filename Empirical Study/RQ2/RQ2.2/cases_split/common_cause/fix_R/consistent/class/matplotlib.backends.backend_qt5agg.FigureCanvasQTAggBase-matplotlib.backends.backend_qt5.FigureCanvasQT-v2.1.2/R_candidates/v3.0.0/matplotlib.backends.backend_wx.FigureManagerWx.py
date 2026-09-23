class FigureManagerWx(FigureManagerBase):
    """
    This class contains the FigureCanvas and GUI frame

    It is instantiated by GcfWx whenever a new figure is created. GcfWx is
    responsible for managing multiple instances of FigureManagerWx.

    Attributes
    ----------
    canvas : `FigureCanvas`
        a FigureCanvasWx(wx.Panel) instance
    window : wxFrame
        a wxFrame instance - wxpython.org/Phoenix/docs/html/Frame.html

    """

    def __init__(self, canvas, num, frame):
        DEBUG_MSG("__init__()", 1, self)
        FigureManagerBase.__init__(self, canvas, num)
        self.frame = frame
        self.window = frame

        self.toolmanager = getattr(frame, "toolmanager", None)
        self.toolbar = frame.GetToolBar()

    def show(self):
        self.frame.Show()
        self.canvas.draw()

    def destroy(self, *args):
        DEBUG_MSG("destroy()", 1, self)
        self.frame.Destroy()
        wxapp = wx.GetApp()
        if wxapp:
            wxapp.Yield()

    def get_window_title(self):
        return self.window.GetTitle()

    def set_window_title(self, title):
        self.window.SetTitle(title)

    def resize(self, width, height):
        'Set the canvas size in pixels'
        self.canvas.SetInitialSize(wx.Size(width, height))
        self.window.GetSizer().Fit(self.window)
