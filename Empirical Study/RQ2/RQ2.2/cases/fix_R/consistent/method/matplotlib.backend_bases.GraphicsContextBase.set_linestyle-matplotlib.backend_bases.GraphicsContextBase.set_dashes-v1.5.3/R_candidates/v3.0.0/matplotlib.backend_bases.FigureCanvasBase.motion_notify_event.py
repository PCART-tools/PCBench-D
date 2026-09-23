    def motion_notify_event(self, x, y, guiEvent=None):
        """
        Backend derived classes should call this function on any
        motion-notify-event.

        This method will call all functions connected to the
        'motion_notify_event' with a :class:`MouseEvent` instance.

        Parameters
        ----------
        x : scalar
            the canvas coordinates where 0=left

        y : scalar
            the canvas coordinates where 0=bottom

        guiEvent
            the native UI event that generated the mpl event

        """
        self._lastx, self._lasty = x, y
        s = 'motion_notify_event'
        event = MouseEvent(s, self, x, y, self._button, self._key,
                           guiEvent=guiEvent)
        self.callbacks.process(s, event)
