    def mouse_event_stop(self, event):
        """Process an button-2 event (end blocking input)."""
        # Remove last event just for cleanliness.
        BlockingInput.pop(self)
        # This will exit even if not in infinite mode.  This is consistent with
        # MATLAB and sometimes quite useful, but will require the user to test
        # how many points were actually returned before using data.
        self.fig.canvas.stop_event_loop()
