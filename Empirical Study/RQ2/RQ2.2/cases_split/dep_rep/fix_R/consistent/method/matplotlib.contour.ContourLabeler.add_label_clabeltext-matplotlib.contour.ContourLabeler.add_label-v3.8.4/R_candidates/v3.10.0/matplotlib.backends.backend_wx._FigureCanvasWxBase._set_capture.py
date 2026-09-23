    def _set_capture(self, capture=True):
        """Control wx mouse capture."""
        if self.HasCapture():
            self.ReleaseMouse()
        if capture:
            self.CaptureMouse()
