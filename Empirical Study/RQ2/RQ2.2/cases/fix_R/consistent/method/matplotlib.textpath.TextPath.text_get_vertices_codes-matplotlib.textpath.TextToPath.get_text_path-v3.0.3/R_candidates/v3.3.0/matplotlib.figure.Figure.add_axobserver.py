    def add_axobserver(self, func):
        """Whenever the axes state change, ``func(self)`` will be called."""
        # Connect a wrapper lambda and not func itself, to avoid it being
        # weakref-collected.
        self._axobservers.connect("_axes_change_event", lambda arg: func(arg))
