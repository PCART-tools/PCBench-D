    def set_heights(self, heights):
        """Set the lengths of second axes (e.g., minor axes)."""
        self._heights = 0.5 * np.asarray(heights).ravel()
        self.stale = True
