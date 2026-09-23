class FigureManagerWx(FigureManagerBase):
    """
    Container/controller for the FigureCanvas and GUI frame.

    It is instantiated by Gcf whenever a new figure is created.  Gcf is
    responsible for managing multiple instances of FigureManagerWx.

    Attributes
    ----------
    canvas : `FigureCanvas`
        a FigureCanvasWx(wx.Panel) instance
    window : wxFrame
        a wxFrame instance - wxpython.org/Phoenix/docs/html/Frame.html
    """

    def __init__(self, canvas, num, frame):
        _log.debug("%s - __init__()", type(self))
        self.frame = self.window = frame
        self._initializing = True
        super().__init__(canvas, num)
        self._initializing = False

    @property
    def toolbar(self):
        return self.frame.GetToolBar()

    @toolbar.setter
    def toolbar(self, value):
        # Never allow this, except that base class inits this to None before
        # the frame is set up.
        if not self._initializing:
            raise AttributeError("can't set attribute")

    def show(self):
        # docstring inherited
        self.frame.Show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            self.frame.Raise()

    def destroy(self, *args):
        # docstring inherited
        _log.debug("%s - destroy()", type(self))
        frame = self.frame
        if frame:  # Else, may have been already deleted, e.g. when closing.
            # As this can be called from non-GUI thread from plt.close use
            # wx.CallAfter to ensure thread safety.
            wx.CallAfter(frame.Close)

    def full_screen_toggle(self):
        # docstring inherited
        self.frame.ShowFullScreen(not self.frame.IsFullScreen())

    def get_window_title(self):
        # docstring inherited
        return self.window.GetTitle()

    def set_window_title(self, title):
        # docstring inherited
        self.window.SetTitle(title)

    def resize(self, width, height):
        # docstring inherited
        self.canvas.SetInitialSize(
            wx.Size(math.ceil(width), math.ceil(height)))
        self.window.GetSizer().Fit(self.window)
