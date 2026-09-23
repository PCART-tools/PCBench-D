    @deprecate_function(
        "Use `Series.dtype.is_integer()` instead."
        " For signed/unsigned variants, use `Series.dtype.is_signed_integer()`"
        " or `Series.dtype.is_unsigned_integer()`.",
        version="0.19.13",
    )
    def is_integer(self, signed: bool | None = None) -> bool:
        """
        Check if this Series datatype is an integer (signed or unsigned).

        .. deprecated:: 0.19.13
            Use `Series.dtype.is_integer()` instead.
            For signed/unsigned variants, use `Series.dtype.is_signed_integer()`
            or `Series.dtype.is_unsigned_integer()`.

        Parameters
        ----------
        signed
            * if `None`, both signed and unsigned integer dtypes will match.
            * if `True`, only signed integer dtypes will be considered a match.
            * if `False`, only unsigned integer dtypes will be considered a match.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3], dtype=pl.UInt32)
        >>> s.is_integer()  # doctest: +SKIP
        True
        >>> s.is_integer(signed=False)  # doctest: +SKIP
        True
        >>> s.is_integer(signed=True)  # doctest: +SKIP
        False
        """
        if signed is None:
            return self.dtype.is_integer()
        elif signed is True:
            return self.dtype.is_signed_integer()
        elif signed is False:
            return self.dtype.is_unsigned_integer()

        msg = f"`signed` must be None, True or False; got {signed!r}"
        raise ValueError(msg)
