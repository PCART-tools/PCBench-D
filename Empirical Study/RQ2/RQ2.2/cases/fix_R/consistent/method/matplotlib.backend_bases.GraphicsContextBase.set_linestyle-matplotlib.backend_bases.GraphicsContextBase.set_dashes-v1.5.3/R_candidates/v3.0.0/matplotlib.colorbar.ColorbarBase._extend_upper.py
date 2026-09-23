    def _extend_upper(self):
        """Returns whether the uper limit is open ended."""
        return self.extend in ('both', 'max')
