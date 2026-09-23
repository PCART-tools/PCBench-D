    @property
    def size(self):
        # type: () -> int
        """The number of elements in this array."""
        return np.prod(self.shape)
