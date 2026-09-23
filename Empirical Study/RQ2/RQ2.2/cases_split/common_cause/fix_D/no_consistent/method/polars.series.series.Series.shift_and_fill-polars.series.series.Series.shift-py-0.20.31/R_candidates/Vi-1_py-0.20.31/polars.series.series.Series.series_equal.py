    @deprecate_renamed_function("equals", version="0.19.16")
    def series_equal(
        self, other: Series, *, null_equal: bool = True, strict: bool = False
    ) -> bool:
        """
        Check whether the Series is equal to another Series.

        .. deprecated:: 0.19.16
            This method has been renamed to :meth:`equals`.

        Parameters
        ----------
        other
            Series to compare with.
        null_equal
            Consider null values as equal.
        strict
            Don't allow different numerical dtypes, e.g. comparing `pl.UInt32` with a
            `pl.Int64` will return `False`.
        """
        return self.equals(other, check_dtypes=strict, null_equal=null_equal)
