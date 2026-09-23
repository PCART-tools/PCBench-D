class TimerGTK3(TimerBase):
    '''
    Subclass of :class:`backend_bases.TimerBase` using GTK3 for timer events.

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
    def _timer_start(self):
        # Need to stop it, otherwise we potentially leak a timer id that will
        # never be stopped.
        self._timer_stop()
        self._timer = GLib.timeout_add(self._interval, self._on_timer)

    def _timer_stop(self):
        if self._timer is not None:
            GLib.source_remove(self._timer)
            self._timer = None

    def _timer_set_interval(self):
        # Only stop and restart it if the timer has already been started
        if self._timer is not None:
            self._timer_stop()
            self._timer_start()

    def _on_timer(self):
        TimerBase._on_timer(self)

        # Gtk timeout_add() requires that the callback returns True if it
        # is to be called again.
        if self.callbacks and not self._single:
            return True
        else:
            self._timer = None
            return False
