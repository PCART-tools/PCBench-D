    def __init__(self, interval=None, callbacks=None):
        """
        Parameters
        ----------
        interval : int, default: 1000ms
            The time between timer events in milliseconds.  Will be stored as
            ``timer.interval``.
        callbacks : list[tuple[callable, tuple, dict]]
            List of (func, args, kwargs) tuples that will be called upon timer
            events.  This list is accessible as ``timer.callbacks`` and can be
            manipulated directly, or the functions `~.TimerBase.add_callback`
            and `~.TimerBase.remove_callback` can be used.
        """
        self.callbacks = [] if callbacks is None else callbacks.copy()
        # Set .interval and not ._interval to go through the property setter.
        self.interval = 1000 if interval is None else interval
        self.single_shot = False
