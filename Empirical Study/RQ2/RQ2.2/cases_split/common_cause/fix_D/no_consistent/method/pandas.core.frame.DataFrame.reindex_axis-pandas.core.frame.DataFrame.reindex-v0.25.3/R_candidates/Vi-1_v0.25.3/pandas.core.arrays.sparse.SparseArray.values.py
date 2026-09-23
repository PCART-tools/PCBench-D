    @property
    def values(self):
        """
        Dense values

        .. deprecated:: 0.25.0

            Use ``np.asarray(...)`` or the ``.to_dense()`` method instead.
        """
        msg = (
            "The SparseArray.values attribute is deprecated and will be "
            "removed in a future version. You can use `np.asarray(...)` or "
            "the `.to_dense()` method instead."
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)
        return self.to_dense()
