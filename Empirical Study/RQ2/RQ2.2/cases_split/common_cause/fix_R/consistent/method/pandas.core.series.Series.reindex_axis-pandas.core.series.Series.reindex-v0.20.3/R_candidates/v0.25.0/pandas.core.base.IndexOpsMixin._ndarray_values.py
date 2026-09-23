    @property
    def _ndarray_values(self) -> np.ndarray:
        """
        The data as an ndarray, possibly losing information.

        The expectation is that this is cheap to compute, and is primarily
        used for interacting with our indexers.

        - categorical -> codes
        """
        if is_extension_array_dtype(self):
            return self.array._ndarray_values
        # As a mixin, we depend on the mixing class having values.
        # Special mixin syntax may be developed in the future:
        # https://github.com/python/typing/issues/246
        return self.values  # type: ignore
