    def __call__(self, n=1, timeout=30):
        """Blocking call to retrieve *n* events."""
        _api.check_isinstance(Integral, n=n)
        self.n = n
        self.events = []

        if hasattr(self.fig.canvas, "manager"):
            # Ensure that the figure is shown, if we are managing it.
            self.fig.show()
        # Connect the events to the on_event function call.
        self.callbacks = [self.fig.canvas.mpl_connect(name, self.on_event)
                          for name in self.eventslist]
        try:
            # Start event loop.
            self.fig.canvas.start_event_loop(timeout=timeout)
        finally:  # Run even on exception like ctrl-c.
            # Disconnect the callbacks.
            self.cleanup()
        # Return the events in this case.
        return self.events
