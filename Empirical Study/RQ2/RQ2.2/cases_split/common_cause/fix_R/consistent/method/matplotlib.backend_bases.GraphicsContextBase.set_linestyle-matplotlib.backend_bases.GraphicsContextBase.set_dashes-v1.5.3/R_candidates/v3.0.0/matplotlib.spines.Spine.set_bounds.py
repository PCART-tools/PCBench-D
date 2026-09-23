    def set_bounds(self, low, high):
        """Set the bounds of the spine."""
        if self.spine_type == 'circle':
            raise ValueError(
                'set_bounds() method incompatible with circular spines')
        self._bounds = (low, high)
        self.stale = True
