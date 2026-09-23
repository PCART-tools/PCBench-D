    def button_release_event(self, x, y, button, guiEvent=None):
        """
        Backend derived classes should call this function on any mouse
        button release.

        This method will call all functions connected to the
        'button_release_event' with a :class:`MouseEvent` instance.

        Parameters
        ----------
        x : scalar
            the canvas coordinates where 0=left

        y : scalar
            the canvas coordinates where 0=bottom

        guiEvent
            the native UI event that generated the mpl event

        """
        s = 'button_release_event'
        event = MouseEvent(s, self, x, y, button, self._key, guiEvent=guiEvent)
        self.callbacks.process(s, event)
        self._button = None
