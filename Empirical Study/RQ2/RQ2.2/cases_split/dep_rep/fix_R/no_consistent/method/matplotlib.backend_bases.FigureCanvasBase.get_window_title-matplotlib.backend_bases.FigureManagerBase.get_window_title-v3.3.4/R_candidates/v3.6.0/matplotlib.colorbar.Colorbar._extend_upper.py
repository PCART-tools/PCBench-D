    def _extend_upper(self):
        """Return whether the upper limit is open ended."""
        minmax = "min" if self._long_axis().get_inverted() else "max"
        return self.extend in ('both', minmax)
