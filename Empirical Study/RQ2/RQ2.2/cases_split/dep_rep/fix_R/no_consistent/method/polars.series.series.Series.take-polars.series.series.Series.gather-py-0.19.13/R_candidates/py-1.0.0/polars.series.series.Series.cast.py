    def cast(
        self,
        dtype: PolarsDataType | type[int] | type[float] | type[str] | type[bool],
        *,
        strict: bool = True,
        wrap_numerical: bool = False,
    ) -> Self:
        r"""
        Cast between data types.

        Parameters
        ----------
        dtype
            DataType to cast to.
        strict
            If True invalid casts generate exceptions instead of `null`\s.
        wrap_numerical
            If True numeric casts wrap overflowing values instead of
            marking the cast as invalid.

        Examples
        --------
        >>> s = pl.Series("a", [True, False, True])
        >>> s
        shape: (3,)
        Series: 'a' [bool]
        [
            true
            false
            true
        ]

        >>> s.cast(pl.UInt32)
        shape: (3,)
        Series: 'a' [u32]
        [
            1
            0
            1
        ]
        """
        # Do not dispatch cast as it is expensive and used in other functions.
        dtype = parse_into_dtype(dtype)
        return self._from_pyseries(self._s.cast(dtype, strict, wrap_numerical))
