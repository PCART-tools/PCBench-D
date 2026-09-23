    def __init__(self, canvas):
        self.canvas = canvas
        canvas.toolbar = self
        self._nav_stack = cbook.Stack()
        self._xypress = None  # location and axis info at the time of the press
        self._idPress = None
        self._idRelease = None
        self._active = None
        # This cursor will be set after the initial draw.
        self._lastCursor = cursors.POINTER
        self._init_toolbar()
        self._idDrag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)

        self._ids_zoom = []
        self._zoom_mode = None

        self._button_pressed = None  # determined by button pressed at start

        self.mode = ''  # a mode string for the status bar
        self.set_history_buttons()
