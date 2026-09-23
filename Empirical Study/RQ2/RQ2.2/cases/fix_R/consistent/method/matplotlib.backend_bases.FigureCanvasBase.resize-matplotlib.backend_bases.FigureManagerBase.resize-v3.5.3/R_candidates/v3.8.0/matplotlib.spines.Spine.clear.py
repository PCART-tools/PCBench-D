    def clear(self):
        """Clear the current spine."""
        self._clear()
        if self.axis is not None:
            self.axis.clear()
