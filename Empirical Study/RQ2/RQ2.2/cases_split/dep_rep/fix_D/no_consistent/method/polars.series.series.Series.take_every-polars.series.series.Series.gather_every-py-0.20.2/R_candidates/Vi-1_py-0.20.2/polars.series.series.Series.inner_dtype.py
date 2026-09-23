    @property
    def inner_dtype(self) -> DataType | None:
        """
        Get the inner dtype in of a List typed Series.

        .. deprecated:: 0.19.14
            Use `Series.dtype.inner` instead.

        Returns
        -------
        DataType

        """
        issue_deprecation_warning(
            "`Series.inner_dtype` is deprecated. Use `Series.dtype.inner` instead.",
            version="0.19.14",
        )
        try:
            return self.dtype.inner  # type: ignore[attr-defined]
        except AttributeError:
            return None
