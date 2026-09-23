    def get_fill(self):
        """Return whether face is colored."""
        return not cbook._str_lower_equal(self._original_facecolor, "none")
