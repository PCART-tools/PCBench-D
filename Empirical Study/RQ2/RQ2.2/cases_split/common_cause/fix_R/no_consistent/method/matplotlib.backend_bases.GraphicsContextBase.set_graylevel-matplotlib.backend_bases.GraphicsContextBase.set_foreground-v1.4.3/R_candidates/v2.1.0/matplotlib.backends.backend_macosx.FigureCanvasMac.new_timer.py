    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of :class:`backend_bases.Timer`.
        This is useful for getting periodic events through the backend's native
        event loop. Implemented only for backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds
        callbacks : list
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.
        """
        return TimerMac(*args, **kwargs)
