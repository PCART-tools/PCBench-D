    def enter_notify_event(self, guiEvent=None, xy=None):
        """
        Backend derived classes should call this function when entering
        canvas

        Parameters
        ----------
        guiEvent
            the native UI event that generated the mpl event
        xy : tuple of 2 scalars
            the coordinate location of the pointer when the canvas is
            entered

        """
        if xy is not None:
            x, y = xy
            self._lastx, self._lasty = x, y

        event = Event('figure_enter_event', self, guiEvent)
        self.callbacks.process('figure_enter_event', event)
