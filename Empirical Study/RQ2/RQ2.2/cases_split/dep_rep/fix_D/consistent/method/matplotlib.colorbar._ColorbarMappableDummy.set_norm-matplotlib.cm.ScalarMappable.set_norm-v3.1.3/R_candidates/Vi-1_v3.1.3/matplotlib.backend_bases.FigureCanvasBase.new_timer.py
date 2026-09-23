    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of
        :class:`backend_bases.Timer`. This is useful for getting periodic
        events through the backend's native event loop. Implemented only for
        backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds

        callbacks : List[Tuple[callable, Tuple, Dict]]
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.

            callbacks which return ``False`` or ``0`` will be removed from the
            timer.

        Examples
        --------

        >>> timer = fig.canvas.new_timer(callbacks=[(f1, (1, ), {'a': 3}),])

        """
        return TimerBase(*args, **kwargs)
