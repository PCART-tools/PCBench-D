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
