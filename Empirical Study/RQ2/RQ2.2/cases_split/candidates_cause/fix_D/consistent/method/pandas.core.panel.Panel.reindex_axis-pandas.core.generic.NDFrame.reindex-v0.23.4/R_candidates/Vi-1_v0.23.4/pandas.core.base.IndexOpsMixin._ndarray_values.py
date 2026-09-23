    @property
    def _ndarray_values(self):
        """The data as an ndarray, possibly losing information.

        The expectation is that this is cheap to compute, and is primarily
        used for interacting with our indexers.

        - categorical -> codes
        """
        # type: () -> np.ndarray
        if is_extension_array_dtype(self):
            return self.values._ndarray_values
        return self.values
