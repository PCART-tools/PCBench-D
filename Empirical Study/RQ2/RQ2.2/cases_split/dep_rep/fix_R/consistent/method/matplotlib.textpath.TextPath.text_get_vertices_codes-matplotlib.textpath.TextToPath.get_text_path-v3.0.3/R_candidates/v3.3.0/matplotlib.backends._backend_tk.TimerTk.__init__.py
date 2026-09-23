    def __init__(self, parent, *args, **kwargs):
        self._timer = None
        TimerBase.__init__(self, *args, **kwargs)
        self.parent = parent
