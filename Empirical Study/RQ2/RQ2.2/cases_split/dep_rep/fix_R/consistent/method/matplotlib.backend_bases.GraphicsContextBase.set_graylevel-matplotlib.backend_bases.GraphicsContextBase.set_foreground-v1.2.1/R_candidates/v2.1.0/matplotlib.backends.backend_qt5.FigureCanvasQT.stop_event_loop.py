    def stop_event_loop(self, event=None):
        if hasattr(self, "_event_loop"):
            self._event_loop.quit()
