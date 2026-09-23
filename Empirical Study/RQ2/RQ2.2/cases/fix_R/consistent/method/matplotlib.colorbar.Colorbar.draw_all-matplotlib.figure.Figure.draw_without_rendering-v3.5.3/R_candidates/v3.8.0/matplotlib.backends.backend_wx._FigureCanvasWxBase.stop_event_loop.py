    def stop_event_loop(self, event=None):
        # docstring inherited
        if hasattr(self, '_event_loop'):
            if self._event_loop.IsRunning():
                self._event_loop.Exit()
            del self._event_loop
