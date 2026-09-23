    @deprecate_renamed_function("count_matches", version="0.19.3")
    def count_match(self, pattern: str | Series) -> Series:
        """
        Count all successive non-overlapping regex matches.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`count_matches`.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_. Can also be a :class:`Series` of
            regular expressions.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`. Returns null if the original
            value is null.
        """
