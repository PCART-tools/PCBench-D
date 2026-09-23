class TimerTk(TimerBase):
    '''
    Subclass of :class:`backend_bases.TimerBase` that uses Tk's timer events.

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
    def __init__(self, parent, *args, **kwargs):
        TimerBase.__init__(self, *args, **kwargs)
        self.parent = parent
        self._timer = None

    def _timer_start(self):
        self._timer_stop()
        self._timer = self.parent.after(self._interval, self._on_timer)

    def _timer_stop(self):
        if self._timer is not None:
            self.parent.after_cancel(self._timer)
        self._timer = None

    def _on_timer(self):
        TimerBase._on_timer(self)

        # Tk after() is only a single shot, so we need to add code here to
        # reset the timer if we're not operating in single shot mode.  However,
        # if _timer is None, this means that _timer_stop has been called; so
        # don't recreate the timer in that case.
        if not self._single and self._timer:
            self._timer = self.parent.after(self._interval, self._on_timer)
        else:
            self._timer = None
