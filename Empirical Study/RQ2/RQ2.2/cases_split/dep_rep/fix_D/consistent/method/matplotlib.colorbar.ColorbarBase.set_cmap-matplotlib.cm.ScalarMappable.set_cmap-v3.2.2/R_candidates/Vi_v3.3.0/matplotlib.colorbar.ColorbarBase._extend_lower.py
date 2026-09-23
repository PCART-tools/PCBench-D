    def _extend_lower(self):
        """Return whether the lower limit is open ended."""
        return self.extend in ('both', 'min')
