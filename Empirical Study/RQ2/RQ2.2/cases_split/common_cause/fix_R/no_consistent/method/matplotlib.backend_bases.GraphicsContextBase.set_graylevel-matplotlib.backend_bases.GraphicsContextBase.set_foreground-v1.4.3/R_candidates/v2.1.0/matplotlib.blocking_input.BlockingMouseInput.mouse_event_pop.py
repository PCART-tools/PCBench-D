    def mouse_event_pop(self, event):
        """
        Will be called for any event involving button 3.
        Button 3 removes the last click.
        """
        # Remove this last event
        BlockingInput.pop(self, -1)

        # Now remove any existing clicks if possible
        if len(self.events) > 0:
            self.pop(event, -1)
