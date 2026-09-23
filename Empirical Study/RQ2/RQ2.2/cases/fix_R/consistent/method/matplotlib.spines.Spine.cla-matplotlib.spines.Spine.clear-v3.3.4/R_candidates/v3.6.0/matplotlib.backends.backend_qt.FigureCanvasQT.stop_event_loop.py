    def stop_event_loop(self, event=None):
        # docstring inherited
        if hasattr(self, "_event_loop"):
            self._event_loop.quit()
