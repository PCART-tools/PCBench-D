    def __call__(self, n=1, timeout=30):
        """
        Blocking call to retrieve n events
        """

        if not isinstance(n, int):
            raise ValueError("Requires an integer argument")
        self.n = n

        self.events = []
        self.callbacks = []

        if hasattr(self.fig, "manager"):
            # Ensure that the figure is shown, if we are managing it.
            self.fig.show()

        # connect the events to the on_event function call
        for n in self.eventslist:
            self.callbacks.append(
                self.fig.canvas.mpl_connect(n, self.on_event))

        try:
            # Start event loop
            self.fig.canvas.start_event_loop(timeout=timeout)
        finally:  # Run even on exception like ctrl-c
            # Disconnect the callbacks
            self.cleanup()

        # Return the events in this case
        return self.events
