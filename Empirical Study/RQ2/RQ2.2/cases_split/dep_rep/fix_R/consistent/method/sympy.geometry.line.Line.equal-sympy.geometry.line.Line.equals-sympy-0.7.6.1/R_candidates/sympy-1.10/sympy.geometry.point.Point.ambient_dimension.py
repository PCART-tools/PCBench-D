    @property
    def ambient_dimension(self):
        """Number of components this point has."""
        return getattr(self, '_ambient_dimension', len(self))
