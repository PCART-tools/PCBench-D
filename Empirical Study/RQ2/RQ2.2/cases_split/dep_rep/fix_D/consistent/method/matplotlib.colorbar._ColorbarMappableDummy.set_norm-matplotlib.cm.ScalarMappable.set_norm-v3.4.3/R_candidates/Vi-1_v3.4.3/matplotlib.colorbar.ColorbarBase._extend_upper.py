    def _extend_upper(self):
        """Return whether the upper limit is open ended."""
        return self.extend in ('both', 'max')
