    def __str__(self):
        """Print the Epoch."""
        return f"{self.julianDate(self._frame):22.15e} {self._frame}"
