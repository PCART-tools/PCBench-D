    def __init__(self, figure=None):
        warnings.warn('Treat the new Tool classes introduced in v1.5 as ' +
                       'experimental for now, the API will likely change in ' +
                       'version 2.1 and perhaps the rcParam as well')

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
