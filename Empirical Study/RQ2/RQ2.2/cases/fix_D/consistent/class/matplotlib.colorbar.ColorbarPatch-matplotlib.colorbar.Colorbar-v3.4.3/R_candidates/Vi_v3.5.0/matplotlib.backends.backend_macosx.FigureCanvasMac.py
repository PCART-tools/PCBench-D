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

    def set_cursor(self, cursor):
        # docstring inherited
        _macosx.set_cursor(cursor)

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
        # Size from macOS is logical pixels, dpi is physical.
        scale = self.figure.dpi / self.device_pixel_ratio
        width /= scale
        height /= scale
        self.figure.set_size_inches(width, height, forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()
