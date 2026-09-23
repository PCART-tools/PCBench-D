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
        self.mouse_grabber = None  # the Axes currently grabbing mouse
        self.toolbar = None  # NavigationToolbar2 will set me
        self._is_idle_drawing = False
        # We don't want to scale up the figure DPI more than once.
        figure._original_dpi = figure.dpi
        self._device_pixel_ratio = 1
        super().__init__()  # Typically the GUI widget init (if any).
