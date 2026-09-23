    @property
    def _ndarray_values(self):
        # type: () -> np.ndarray
        """
        The data as an ndarray, possibly losing information.

        The expectation is that this is cheap to compute, and is primarily
        used for interacting with our indexers.

        - categorical -> codes
        """
        if is_extension_array_dtype(self):
            return self.array._ndarray_values
        return self.values
