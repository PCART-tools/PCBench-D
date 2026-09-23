    def __init__(self, figure=None):

        self._key_press_handler_id = None

        self._tools = {}
        self._keys = {}
        self._toggled = {}
        self._callbacks = cbook.CallbackRegistry()

        # to process keypress event
        self.keypresslock = widgets.LockDraw()
        self.messagelock = widgets.LockDraw()

        self._figure = None
        self.set_figure(figure)
