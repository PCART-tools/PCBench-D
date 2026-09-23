    def cla(self):
        """Clear the current spine."""
        self._position = None  # clear position
        if self.axis is not None:
            self.axis.cla()
