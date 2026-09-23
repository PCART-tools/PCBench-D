    def put(self, *args, **kwargs):
        """
        Apply the `put` method to its `values` attribute if it has one.

        .. deprecated:: 0.25.0

        See Also
        --------
        numpy.ndarray.put
        """
        warnings.warn(
            "`put` has been deprecated and will be removed in a" "future version.",
            FutureWarning,
            stacklevel=2,
        )
        self._values.put(*args, **kwargs)
