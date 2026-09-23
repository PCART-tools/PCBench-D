    def cast(
        self,
        dtype: (PolarsDataType | type[int] | type[float] | type[str] | type[bool]),
        *,
        strict: bool = True,
    ) -> Self:
        """
        Cast between data types.

        Parameters
        ----------
        dtype
            DataType to cast to.
        strict
            Throw an error if a cast could not be done (for instance, due to an
            overflow).

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
        dtype = py_type_to_dtype(dtype)
        return self._from_pyseries(self._s.cast(dtype, strict))
