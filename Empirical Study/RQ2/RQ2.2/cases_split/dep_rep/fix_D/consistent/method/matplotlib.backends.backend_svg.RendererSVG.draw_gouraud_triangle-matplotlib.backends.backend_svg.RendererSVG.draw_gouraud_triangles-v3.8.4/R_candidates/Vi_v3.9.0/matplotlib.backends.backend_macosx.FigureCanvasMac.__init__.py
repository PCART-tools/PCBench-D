    def __init__(self, figure):
        super().__init__(figure=figure)
        self._draw_pending = False
        self._is_drawing = False
        # Keep track of the timers that are alive
        self._timers = set()
