    @_api.deprecated("3.6", alternative=(
        "callbacks.process('enter_notify_event', LocationEvent(...))"))
    def enter_notify_event(self, guiEvent=None, *, xy):
        """
        Callback processing for the mouse cursor entering the canvas.

        Backend derived classes should call this function when entering
        canvas.

        Parameters
        ----------
        guiEvent
            The native UI event that generated the Matplotlib event.
        xy : (float, float)
            The coordinate location of the pointer when the canvas is entered.
        """
        self._lastx, self._lasty = x, y = xy
        event = LocationEvent('figure_enter_event', self, x, y, guiEvent)
        self.callbacks.process('figure_enter_event', event)
