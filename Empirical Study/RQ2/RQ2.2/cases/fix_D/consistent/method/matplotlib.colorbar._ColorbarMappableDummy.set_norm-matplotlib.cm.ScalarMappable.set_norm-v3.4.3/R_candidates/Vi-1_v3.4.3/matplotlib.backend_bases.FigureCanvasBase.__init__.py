    def __init__(self, figure=None):
        from matplotlib.figure import Figure
        self._fix_ipython_backend2gui()
        self._is_idle_drawing = True
        self._is_saving = False
        if figure is None:
            figure = Figure()
        figure.set_canvas(self)
        self.figure = figure
        self.manager = None
        self.widgetlock = widgets.LockDraw()
        self._button = None  # the button pressed
        self._key = None  # the key pressed
        self._lastx, self._lasty = None, None
        self.mouse_grabber = None  # the axes currently grabbing mouse
        self.toolbar = None  # NavigationToolbar2 will set me
        self._is_idle_drawing = False
