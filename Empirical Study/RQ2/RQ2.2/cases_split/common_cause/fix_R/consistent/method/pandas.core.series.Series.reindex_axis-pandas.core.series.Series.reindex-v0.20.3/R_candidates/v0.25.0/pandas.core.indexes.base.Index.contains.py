    def contains(self, key):
        """
        Return a boolean indicating whether the provided key is in the index.

        .. deprecated:: 0.25.0
            Use ``key in index`` instead of ``index.contains(key)``.

        Returns
        -------
        bool
        """
        warnings.warn(
            "The 'contains' method is deprecated and will be removed in a "
            "future version. Use 'key in index' instead of "
            "'index.contains(key)'",
            FutureWarning,
            stacklevel=2,
        )
        return key in self
