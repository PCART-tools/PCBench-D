    def __init__(self, figure):
        self._is_idle_drawing = True
        self._is_saving = False
        figure.set_canvas(self)
        self.figure = figure
        # a dictionary from event name to a dictionary that maps cid->func
        self.callbacks = cbook.CallbackRegistry()
        self.widgetlock = widgets.LockDraw()
        self._button = None  # the button pressed
        self._key = None  # the key pressed
        self._lastx, self._lasty = None, None
        self.button_pick_id = self.mpl_connect('button_press_event', self.pick)
        self.scroll_pick_id = self.mpl_connect('scroll_event', self.pick)
        self.mouse_grabber = None  # the axes currently grabbing mouse
        self.toolbar = None  # NavigationToolbar2 will set me
        self._is_idle_drawing = False
