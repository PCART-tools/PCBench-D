    @property
    def ftype(self):
        """
        Return if the data is sparse|dense.

        .. deprecated:: 0.25.0
           Use :func:`dtype` instead.
        """
        warnings.warn(
            "Series.ftype is deprecated and will "
            "be removed in a future version. "
            "Use Series.dtype instead.",
            FutureWarning,
            stacklevel=2,
        )

        return self._data.ftype
