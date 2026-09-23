    def enter_notify_event(self, guiEvent=None, xy=None):
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
        if xy is not None:
            x, y = xy
            self._lastx, self._lasty = x, y
        else:
            x = None
            y = None
            cbook.warn_deprecated(
                '3.0', removal='3.5', name='enter_notify_event',
                message='Since %(since)s, %(name)s expects a location but '
                'your backend did not pass one. This will become an error '
                '%(removal)s.')

        event = LocationEvent('figure_enter_event', self, x, y, guiEvent)
        self.callbacks.process('figure_enter_event', event)
