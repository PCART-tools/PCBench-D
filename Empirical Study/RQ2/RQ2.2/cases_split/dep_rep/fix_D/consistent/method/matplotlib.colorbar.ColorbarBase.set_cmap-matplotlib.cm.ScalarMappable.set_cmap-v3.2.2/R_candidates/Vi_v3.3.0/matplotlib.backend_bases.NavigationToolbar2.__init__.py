    def __init__(self, canvas):
        self.canvas = canvas
        canvas.toolbar = self
        self._nav_stack = cbook.Stack()
        self._xypress = None  # location and axis info at the time of the press
        # This cursor will be set after the initial draw.
        self._lastCursor = cursors.POINTER

        init = cbook._deprecate_method_override(
            __class__._init_toolbar, self, allow_empty=True, since="3.3",
            addendum="Please fully initialize the toolbar in your subclass' "
            "__init__; a fully empty _init_toolbar implementation may be kept "
            "for compatibility with earlier versions of Matplotlib.")
        if init:
            init()

        self._id_press = self.canvas.mpl_connect(
            'button_press_event', self._zoom_pan_handler)
        self._id_release = self.canvas.mpl_connect(
            'button_release_event', self._zoom_pan_handler)
        self._id_drag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        self._zoom_info = None

        self._button_pressed = None  # determined by button pressed at start

        self.mode = _Mode.NONE  # a mode string for the status bar
        self.set_history_buttons()
