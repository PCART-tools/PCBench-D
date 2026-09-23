class FigureCanvasMac(_macosx.FigureCanvas, FigureCanvasAgg):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc...

    Events such as button presses, mouse movements, and key presses
    are handled in the C code and the base class methods
    button_press_event, button_release_event, motion_notify_event,
    key_press_event, and key_release_event are called from there.

    Attributes
    ----------
    figure : `matplotlib.figure.Figure`
        A high-level Figure instance

    """

    def __init__(self, figure):
        FigureCanvasBase.__init__(self, figure)
        width, height = self.get_width_height()
        _macosx.FigureCanvas.__init__(self, width, height)
        self._device_scale = 1.0

    def _set_device_scale(self, value):
        if self._device_scale != value:
            self.figure.dpi = self.figure.dpi / self._device_scale * value
            self._device_scale = value

    def _draw(self):
        renderer = self.get_renderer(cleared=self.figure.stale)

        if self.figure.stale:
            self.figure.draw(renderer)

        return renderer

    def draw(self):
        self.invalidate()
        self.flush_events()

    def draw_idle(self, *args, **kwargs):
        self.invalidate()

    def blit(self, bbox=None):
        self.invalidate()

    def resize(self, width, height):
        dpi = self.figure.dpi
        width /= dpi
        height /= dpi
        self.figure.set_size_inches(width * self._device_scale,
                                    height * self._device_scale,
                                    forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()

    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of `backend_bases.Timer`.
        This is useful for getting periodic events through the backend's native
        event loop. Implemented only for backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds
        callbacks : list
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.
        """
        return TimerMac(*args, **kwargs)
