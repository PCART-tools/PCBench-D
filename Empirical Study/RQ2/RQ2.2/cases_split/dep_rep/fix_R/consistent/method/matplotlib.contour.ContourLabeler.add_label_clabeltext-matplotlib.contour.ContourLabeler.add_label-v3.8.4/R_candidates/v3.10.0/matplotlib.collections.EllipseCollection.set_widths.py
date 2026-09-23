    def set_widths(self, widths):
        """Set the lengths of the first axes (e.g., major axis)."""
        self._widths = 0.5 * np.asarray(widths).ravel()
        self.stale = True
