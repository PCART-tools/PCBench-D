    def __init__(self, *args, **kwargs):
        self._timer = wx.Timer()
        self._timer.Notify = self._on_timer
        super().__init__(*args, **kwargs)
