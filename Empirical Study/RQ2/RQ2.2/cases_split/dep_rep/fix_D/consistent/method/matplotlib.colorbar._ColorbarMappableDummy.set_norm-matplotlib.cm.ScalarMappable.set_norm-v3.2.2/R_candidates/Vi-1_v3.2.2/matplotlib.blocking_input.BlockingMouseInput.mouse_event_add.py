    def mouse_event_add(self, event):
        """
        Process an button-1 event (add a click if inside axes).

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        if event.inaxes:
            self.add_click(event)
        else:  # If not a valid click, remove from event list.
            BlockingInput.pop(self)
