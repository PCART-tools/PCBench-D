    def __init__(self, interval=None, callbacks=None):
        #Initialize empty callbacks list and setup default settings if necssary
        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks[:]  # Create a copy

        if interval is None:
            self._interval = 1000
        else:
            self._interval = interval

        self._single = False

        # Default attribute for holding the GUI-specific timer object
        self._timer = None
