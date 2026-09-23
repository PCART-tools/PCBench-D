    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], wx.EvtHandler):
            cbook.warn_deprecated(
                "3.0", message="Passing a wx.EvtHandler as first argument to "
                "the TimerWx constructor is deprecated since %(since)s.")
            args = args[1:]
        TimerBase.__init__(self, *args, **kwargs)
        self._timer = wx.Timer()
        self._timer.Notify = self._on_timer
