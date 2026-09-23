    def _extend_lower(self):
        """Return whether the lower limit is open ended."""
        minmax = "max" if self.long_axis.get_inverted() else "min"
        return self.extend in ('both', minmax)
