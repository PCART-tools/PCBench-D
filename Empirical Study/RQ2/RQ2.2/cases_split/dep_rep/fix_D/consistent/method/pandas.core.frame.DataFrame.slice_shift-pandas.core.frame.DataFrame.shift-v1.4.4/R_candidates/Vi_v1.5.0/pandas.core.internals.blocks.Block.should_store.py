    @final
    def should_store(self, value: ArrayLike) -> bool:
        """
        Should we set self.values[indexer] = value inplace or do we need to cast?

        Parameters
        ----------
        value : np.ndarray or ExtensionArray

        Returns
        -------
        bool
        """
        # faster equivalent to is_dtype_equal(value.dtype, self.dtype)
        try:
            return value.dtype == self.dtype
        except TypeError:
            return False
