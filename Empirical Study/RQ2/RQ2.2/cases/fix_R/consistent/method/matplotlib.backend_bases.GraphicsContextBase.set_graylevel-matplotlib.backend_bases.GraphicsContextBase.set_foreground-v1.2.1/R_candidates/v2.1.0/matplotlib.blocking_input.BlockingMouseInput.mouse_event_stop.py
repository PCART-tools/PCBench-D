    def mouse_event_stop(self, event):
        """
        Will be called for any event involving button 2.
        Button 2 ends blocking input.
        """

        # Remove last event just for cleanliness
        BlockingInput.pop(self, -1)

        # This will exit even if not in infinite mode.  This is
        # consistent with MATLAB and sometimes quite useful, but will
        # require the user to test how many points were actually
        # returned before using data.
        self.fig.canvas.stop_event_loop()
