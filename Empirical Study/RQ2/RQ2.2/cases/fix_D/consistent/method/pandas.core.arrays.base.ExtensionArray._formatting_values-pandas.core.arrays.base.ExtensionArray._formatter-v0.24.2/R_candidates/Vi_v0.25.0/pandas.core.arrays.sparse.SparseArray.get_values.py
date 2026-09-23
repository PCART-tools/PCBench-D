    def get_values(self):
        """
        Convert SparseArray to a NumPy array.

        .. deprecated:: 0.25.0
            Use `to_dense` instead.

        """
        warnings.warn(
            "The 'get_values' method is deprecated and will be removed in a "
            "future version. Use the 'to_dense' method instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._internal_get_values()
