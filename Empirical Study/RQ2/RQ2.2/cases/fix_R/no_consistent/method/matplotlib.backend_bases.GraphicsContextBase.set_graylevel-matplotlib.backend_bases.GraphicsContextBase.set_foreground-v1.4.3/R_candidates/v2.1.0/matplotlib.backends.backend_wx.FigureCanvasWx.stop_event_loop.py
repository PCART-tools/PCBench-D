    def stop_event_loop(self, event=None):
        """
        Stop an event loop.  This is used to stop a blocking event
        loop so that interactive functions, such as ginput and
        waitforbuttonpress, can wait for events.

        """
        if hasattr(self, '_event_loop'):
            if self._event_loop.IsRunning():
                self._event_loop.Exit()
            del self._event_loop
