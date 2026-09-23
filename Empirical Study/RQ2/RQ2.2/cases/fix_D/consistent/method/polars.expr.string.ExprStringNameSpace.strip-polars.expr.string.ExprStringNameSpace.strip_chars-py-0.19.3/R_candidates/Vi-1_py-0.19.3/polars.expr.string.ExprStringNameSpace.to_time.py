    def to_time(
        self,
        format: str | None = None,
        *,
        strict: bool = True,
        cache: bool = True,
    ) -> Expr:
        """
        Convert a Utf8 column into a Time column.

        Parameters
        ----------
        format
            Format to use for conversion. Refer to the `chrono crate documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for the full specification. Example: ``"%H:%M:%S"``.
            If set to None (default), the format is inferred from the data.
        strict
            Raise an error if any conversion fails.
        cache
            Use a cache of unique, converted times to apply the conversion.

        Examples
        --------
        >>> s = pl.Series(["01:00", "02:00", "03:00"])
        >>> s.str.to_time("%H:%M")
        shape: (3,)
        Series: '' [time]
        [
                01:00:00
                02:00:00
                03:00:00
        ]

        """
        _validate_format_argument(format)
        return wrap_expr(self._pyexpr.str_to_time(format, strict, cache))
