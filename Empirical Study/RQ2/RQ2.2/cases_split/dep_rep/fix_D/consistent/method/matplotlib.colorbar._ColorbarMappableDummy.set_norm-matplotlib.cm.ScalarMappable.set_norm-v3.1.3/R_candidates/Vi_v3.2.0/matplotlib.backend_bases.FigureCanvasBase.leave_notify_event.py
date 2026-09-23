    def leave_notify_event(self, guiEvent=None):
        """
        Backend derived classes should call this function when leaving
        canvas

        Parameters
        ----------
        guiEvent
            The native UI event that generated the Matplotlib event.
        """
        self.callbacks.process('figure_leave_event', LocationEvent.lastevent)
        LocationEvent.lastevent = None
        self._lastx, self._lasty = None, None
