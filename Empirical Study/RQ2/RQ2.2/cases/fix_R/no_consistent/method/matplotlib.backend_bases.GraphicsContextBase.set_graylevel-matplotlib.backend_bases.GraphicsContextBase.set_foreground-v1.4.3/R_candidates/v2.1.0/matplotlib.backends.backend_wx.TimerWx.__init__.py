    def __init__(self, parent, *args, **kwargs):
        TimerBase.__init__(self, *args, **kwargs)

        # Create a new timer and connect the timer event to our handler.
        # For WX, the events have to use a widget for binding.
        self.parent = parent
        self._timer = wx.Timer(self.parent, wx.NewId())
        self.parent.Bind(wx.EVT_TIMER, self._on_timer, self._timer)
