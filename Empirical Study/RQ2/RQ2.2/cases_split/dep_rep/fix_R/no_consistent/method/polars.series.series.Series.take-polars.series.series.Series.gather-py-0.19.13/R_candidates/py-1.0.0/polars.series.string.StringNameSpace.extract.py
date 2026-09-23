    def extract(self, pattern: IntoExprColumn, group_index: int = 1) -> Series:
        r"""
        Extract the target capture group from provided patterns.

        Parameters
        ----------
        pattern
            A valid regular expression pattern containing at least one capture group,
            compatible with the `regex crate <https://docs.rs/regex/latest/regex/>`_.
        group_index
            Index of the targeted capture group.
            Group 0 means the whole pattern, the first group begins at index 1.
            Defaults to the first capture group.

        Returns
        -------
        Series
            Series of data type :class:`String`. Contains null values if the original
            value is null or regex captures nothing.

        Notes
        -----
        To modify regular expression behaviour (such as multi-line matching)
        with flags, use the inline `(?iLmsuxU)` syntax. For example:

        >>> s = pl.Series(
        ...     name="lines",
        ...     values=[
        ...         "I Like\nThose\nOdds",
        ...         "This is\nThe Way",
        ...     ],
        ... )
        >>> s.str.extract(r"(?m)^(T\w+)", 1).alias("matches")
        shape: (2,)
        Series: 'matches' [str]
        [
            "Those"
            "This"
        ]

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        Examples
        --------
        >>> s = pl.Series(
        ...     name="url",
        ...     values=[
        ...         "http://vote.com/ballon_dor?ref=polars&candidate=messi",
        ...         "http://vote.com/ballon_dor?candidate=ronaldo&ref=polars",
        ...         "http://vote.com/ballon_dor?error=404&ref=unknown",
        ...     ],
        ... )
        >>> s.str.extract(r"candidate=(\w+)", 1).alias("candidate")
        shape: (3,)
        Series: 'candidate' [str]
        [
            "messi"
            "ronaldo"
            null
        ]
        """
