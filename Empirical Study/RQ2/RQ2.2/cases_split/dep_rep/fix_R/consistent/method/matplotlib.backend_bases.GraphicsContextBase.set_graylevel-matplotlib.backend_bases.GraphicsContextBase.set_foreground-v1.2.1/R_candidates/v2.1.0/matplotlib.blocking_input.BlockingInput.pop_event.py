    def pop_event(self, index=-1):
        """
        This removes an event from the event list.  Defaults to
        removing last event, but an index can be supplied.  Note that
        this does not check that there are events, much like the
        normal pop method.  If not events exist, this will throw an
        exception.
        """
        self.events.pop(index)
