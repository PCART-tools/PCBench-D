    def onmove(self, event):
        """Cursor move event handler and validator."""
        if not self.ignore(event) and self.eventpress:
            event = self._clean_event(event)
            self._onmove(event)
            return True
        return False
