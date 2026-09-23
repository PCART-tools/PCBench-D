class TimerWx(TimerBase):
    '''
    Subclass of :class:`backend_bases.TimerBase` that uses WxTimer events.

    Attributes
    ----------
    interval : int
        The time between timer events in milliseconds. Default is 1000 ms.
    single_shot : bool
        Boolean flag indicating whether this timer should operate as single
        shot (run once and then stop). Defaults to False.
    callbacks : list
        Stores list of (func, args) tuples that will be called upon timer
        events. This list can be manipulated directly, or the functions
        `add_callback` and `remove_callback` can be used.

    '''

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], wx.EvtHandler):
            cbook.warn_deprecated(
                "3.0", "Passing a wx.EvtHandler as first argument to the "
                "TimerWx constructor is deprecated since %(version)s.")
            args = args[1:]
        TimerBase.__init__(self, *args, **kwargs)
        self._timer = wx.Timer()
        self._timer.Notify = self._on_timer

    def _timer_start(self):
        self._timer.Start(self._interval, self._single)

    def _timer_stop(self):
        self._timer.Stop()

    def _timer_set_interval(self):
        self._timer_start()

    def _timer_set_single_shot(self):
        self._timer.Start()
