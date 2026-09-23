    @property
    def asi8(self):
        """
        Integer representation of the values.

        Returns
        -------
        ndarray
            An ndarray with int64 dtype.
        """
        warnings.warn(
            "Index.asi8 is deprecated and will be removed in a future version",
            FutureWarning,
            stacklevel=2,
        )
        return None
