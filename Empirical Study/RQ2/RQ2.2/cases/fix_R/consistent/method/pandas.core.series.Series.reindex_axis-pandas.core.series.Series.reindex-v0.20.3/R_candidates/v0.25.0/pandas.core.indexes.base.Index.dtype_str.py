    @property
    def dtype_str(self):
        """
        Return the dtype str of the underlying data.

        .. deprecated:: 0.25.0
        """
        warnings.warn(
            "`dtype_str` has been deprecated. Call `str` on the "
            "dtype attribute instead.",
            FutureWarning,
            stacklevel=2,
        )
        return str(self.dtype)
