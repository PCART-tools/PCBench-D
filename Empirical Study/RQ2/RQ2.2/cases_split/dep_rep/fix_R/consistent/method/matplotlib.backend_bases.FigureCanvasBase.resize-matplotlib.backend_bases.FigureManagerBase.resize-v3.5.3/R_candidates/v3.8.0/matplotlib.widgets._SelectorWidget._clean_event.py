    def _clean_event(self, event):
        """
        Preprocess an event:

        - Replace *event* by the previous event if *event* has no ``xdata``.
        - Get ``xdata`` and ``ydata`` from this widget's axes, and clip them to the axes
          limits.
        - Update the previous event.
        """
        if event.xdata is None:
            event = self._prev_event
        else:
            event = copy.copy(event)
        event.xdata, event.ydata = self._get_data(event)
        self._prev_event = event
        return event
