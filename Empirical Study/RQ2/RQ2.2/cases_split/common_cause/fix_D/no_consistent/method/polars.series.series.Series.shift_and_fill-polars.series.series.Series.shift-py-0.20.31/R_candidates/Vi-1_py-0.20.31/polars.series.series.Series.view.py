    @deprecate_function(
        "Use `Series.to_numpy(allow_copy=False) instead.", version="0.19.14"
    )
    def view(self, *, ignore_nulls: bool = False) -> SeriesView:
        """
        Get a view into this Series data with a numpy array.

        .. deprecated:: 0.19.14
            This method will be removed in a future version.

        This operation doesn't clone data, but does not include missing values.
        Don't use this unless you know what you are doing.

        Parameters
        ----------
        ignore_nulls
            If True then nulls are converted to 0.
            If False then an Exception is raised if nulls are present.
        """
        if not ignore_nulls:
            assert not self.null_count()

        from polars.series._numpy import SeriesView, _ptr_to_numpy

        ptr_type = dtype_to_ctype(self.dtype)
        ptr = self._s.as_single_ptr()
        array = _ptr_to_numpy(ptr, self.len(), ptr_type)
        array.setflags(write=False)
        return SeriesView(array, self)
