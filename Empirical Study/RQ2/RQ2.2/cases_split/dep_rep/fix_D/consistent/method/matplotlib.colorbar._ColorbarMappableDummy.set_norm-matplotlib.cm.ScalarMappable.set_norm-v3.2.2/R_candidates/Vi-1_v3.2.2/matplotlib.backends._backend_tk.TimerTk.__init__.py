    def __init__(self, parent, *args, **kwargs):
        TimerBase.__init__(self, *args, **kwargs)
        self.parent = parent
        self._timer = None
