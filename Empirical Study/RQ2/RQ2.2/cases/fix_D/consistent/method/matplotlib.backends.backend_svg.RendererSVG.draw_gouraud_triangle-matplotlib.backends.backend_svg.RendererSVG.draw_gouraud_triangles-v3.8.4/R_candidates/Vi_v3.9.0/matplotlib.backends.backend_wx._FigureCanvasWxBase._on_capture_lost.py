    def _on_capture_lost(self, event):
        """Capture changed or lost"""
        self._set_capture(False)
