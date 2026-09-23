    def button_release_event(self, x, y, button, guiEvent=None):
        """
        Callback processing for mouse button release events.

        Backend derived classes should call this function on any mouse
        button release.

        This method will call all functions connected to the
        'button_release_event' with a `MouseEvent` instance.

        Parameters
        ----------
        x : float
            The canvas coordinates where 0=left.
        y : float
            The canvas coordinates where 0=bottom.
        guiEvent
            The native UI event that generated the Matplotlib event.
        """
        s = 'button_release_event'
        event = MouseEvent(s, self, x, y, button, self._key, guiEvent=guiEvent)
        self.callbacks.process(s, event)
        self._button = None
