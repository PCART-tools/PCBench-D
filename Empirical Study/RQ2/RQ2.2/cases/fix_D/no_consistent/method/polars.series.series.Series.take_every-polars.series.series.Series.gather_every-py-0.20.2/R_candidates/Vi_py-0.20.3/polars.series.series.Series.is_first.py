    @deprecate_renamed_function("is_first_distinct", version="0.19.3")
    def is_first(self) -> Series:
        """
        Return a boolean mask indicating the first occurrence of each distinct value.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`Series.is_first_distinct`.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        """
