    @property
    def ftypes(self):
        """
        Return if the data is sparse|dense.

        .. deprecated:: 0.25.0
           Use :func:`dtypes` instead.
        """
        warnings.warn(
            "Series.ftypes is deprecated and will "
            "be removed in a future version. "
            "Use Series.dtype instead.",
            FutureWarning,
            stacklevel=2,
        )

        return self._data.ftype
