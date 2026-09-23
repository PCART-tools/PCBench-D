class BlockingInput:
    """Callable for retrieving events in a blocking way."""

    def __init__(self, fig, eventslist=()):
        self.fig = fig
        self.eventslist = eventslist

    def on_event(self, event):
        """
        Event handler; will be passed to the current figure to retrieve events.
        """
        # Add a new event to list - using a separate function is overkill for
        # the base class, but this is consistent with subclasses.
        self.add_event(event)
        _log.info("Event %i", len(self.events))

        # This will extract info from events.
        self.post_event()

        # Check if we have enough events already.
        if len(self.events) >= self.n > 0:
            self.fig.canvas.stop_event_loop()

    def post_event(self):
        """For baseclass, do nothing but collect events."""

    def cleanup(self):
        """Disconnect all callbacks."""
        for cb in self.callbacks:
            self.fig.canvas.mpl_disconnect(cb)
        self.callbacks = []

    def add_event(self, event):
        """For base class, this just appends an event to events."""
        self.events.append(event)

    def pop_event(self, index=-1):
        """
        Remove an event from the event list -- by default, the last.

        Note that this does not check that there are events, much like the
        normal pop method.  If no events exist, this will throw an exception.
        """
        self.events.pop(index)

    pop = pop_event

    def __call__(self, n=1, timeout=30):
        """Blocking call to retrieve *n* events."""
        _api.check_isinstance(Integral, n=n)
        self.n = n
        self.events = []

        if self.fig.canvas.manager:
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
