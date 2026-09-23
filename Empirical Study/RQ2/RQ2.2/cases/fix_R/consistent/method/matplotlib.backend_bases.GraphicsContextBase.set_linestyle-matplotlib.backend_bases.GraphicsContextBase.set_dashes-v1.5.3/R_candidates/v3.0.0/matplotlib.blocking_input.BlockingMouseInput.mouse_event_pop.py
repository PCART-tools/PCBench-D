    def mouse_event_pop(self, event):
        """Process an button-3 event (remove the last click)."""
        # Remove this last event.
        BlockingInput.pop(self)
        # Now remove any existing clicks if possible.
        if self.events:
            self.pop(event)
