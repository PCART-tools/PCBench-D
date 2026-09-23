    def _clean_event(self, event):
        """Clean up an event

        Use prev event if there is no xdata
        Limit the xdata and ydata to the axes limits
        Set the prev event
        """
        if event.xdata is None:
            event = self._prev_event
        else:
            event = copy.copy(event)
        event.xdata, event.ydata = self._get_data(event)

        self._prev_event = event
        return event
