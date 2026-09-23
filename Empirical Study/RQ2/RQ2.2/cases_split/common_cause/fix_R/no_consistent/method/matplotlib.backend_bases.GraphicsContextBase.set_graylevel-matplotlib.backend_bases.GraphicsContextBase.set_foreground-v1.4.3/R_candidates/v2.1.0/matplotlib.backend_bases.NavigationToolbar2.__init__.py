    def __init__(self, canvas):
        self.canvas = canvas
        canvas.toolbar = self
        # a dict from axes index to a list of view limits
        self._views = cbook.Stack()
        self._positions = cbook.Stack()  # stack of subplot positions
        self._xypress = None  # the location and axis info at the time
                              # of the press
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

        self._button_pressed = None  # determined by the button pressed
                                     # at start

        self.mode = ''  # a mode string for the status bar
        self.set_history_buttons()

        @partial(canvas.mpl_connect, 'draw_event')
        def define_home(event):
            self.push_current()
            # The decorator sets `define_home` to the callback cid, so we can
            # disconnect it after the first use.
            canvas.mpl_disconnect(define_home)
