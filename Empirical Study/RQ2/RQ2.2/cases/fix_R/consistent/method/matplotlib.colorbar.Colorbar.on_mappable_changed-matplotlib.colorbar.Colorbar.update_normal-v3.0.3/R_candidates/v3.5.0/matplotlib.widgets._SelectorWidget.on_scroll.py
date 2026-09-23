    def on_scroll(self, event):
        """Mouse scroll event handler and validator."""
        if not self.ignore(event):
            self._on_scroll(event)
