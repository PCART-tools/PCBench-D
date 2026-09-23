class FigureCanvasMac(_macosx.FigureCanvas, FigureCanvasAgg):
    # docstring inherited

    # Events such as button presses, mouse movements, and key presses
    # are handled in the C code and the base class methods
    # button_press_event, button_release_event, motion_notify_event,
    # key_press_event, and key_release_event are called from there.

    required_interactive_framework = "macosx"
    _timer_cls = TimerMac

    def __init__(self, figure):
        FigureCanvasBase.__init__(self, figure)
        width, height = self.get_width_height()
        _macosx.FigureCanvas.__init__(self, width, height)
        self._dpi_ratio = 1.0

    def _set_device_scale(self, value):
        if self._dpi_ratio != value:
            # Need the new value in place before setting figure.dpi, which
            # will trigger a resize
            self._dpi_ratio, old_value = value, self._dpi_ratio
            self.figure.dpi = self.figure.dpi / old_value * self._dpi_ratio

    def _draw(self):
        renderer = self.get_renderer(cleared=self.figure.stale)
        if self.figure.stale:
            self.figure.draw(renderer)
        return renderer

    def draw(self):
        # docstring inherited
        self.draw_idle()
        self.flush_events()

    # draw_idle is provided by _macosx.FigureCanvas

    def blit(self, bbox=None):
        self.draw_idle()

    def resize(self, width, height):
        dpi = self.figure.dpi
        width /= dpi
        height /= dpi
        self.figure.set_size_inches(width * self._dpi_ratio,
                                    height * self._dpi_ratio,
                                    forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()
