    @deprecate_renamed_function("is_last_distinct", version="0.19.3")
    def is_last(self) -> Series:
        """
        Return a boolean mask indicating the last occurrence of each distinct value.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`Series.is_last_distinct`.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        """
