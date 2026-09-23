    def enter_notify_event(self, guiEvent=None, xy=None):
        """
        Backend derived classes should call this function when entering
        canvas

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
                '3.0', message='enter_notify_event expects a location but '
                'your backend did not pass one.')

        event = LocationEvent('figure_enter_event', self, x, y, guiEvent)
        self.callbacks.process('figure_enter_event', event)
